#!/bin/bash

# verbit - Utility to parse a Linux Alsa Codec Dump and display the verbs used.
#          Some basic verb modifications needed for AppleHDA are displayed as well.
#
#          version 1.0 - This version assists with simple verb decoding and it is
#                        up to the user to choose which nodes and any final modifications
#                        to make.
#
# Many Thanks to THe KiNG  
# Signal64                        

blacklist[0]="411111f0"
blacklist[1]="400000f0"
blacklist[2]="CD at Int ATAPI"

codecfile=$1
debug=$(dirname $1)/verbitdebug.txt

typeset -i i=0
typeset -i j=0
typeset -i verbcount=0
typeset -i nextassoc=0

brk="--------------------------------------------------------------------------------------------------------"

if [[ ! -f $codecfile ]];then
   echo "ERROR: Could not find codec dump file: $codecfile"
   exit
fi

# Simple check to see if this is a ALSA codec dump file
chk=`head -4 $codecfile | sed '/AFG Function Id/d' | cut -f1 -d":" | tr "\n" " " | tr -d " "`

if [[ $chk != "CodecAddressVendorId" ]];then
   echo "ERROR: This doesn't appear to be an alsa codec dump file"
   head -4 $codecfile
   exit
fi

####################################################################
# Start - Parse and display original codec info from file

> $debug
echo -e "\nVerbs from Linux Codec Dump File: $codecfile"

codecname=`head $codecfile | grep Codec: | cut -f2 -d":" | cut -f2- -d" "`
codecaddr=`head $codecfile | grep Address: | cut -f2 -d":"`
codechex=`head $codecfile | grep "Vendor Id:" | cut -f2 -d":"`
codecdec=`printf "%d" $codechex`

printf "\nCodec: %s   Address: %s   DevID: %s (%s)\n" "$codecname" $codecaddr $codecdec $codechex

echo -e "\n   Jack   Color  Description                  Node     PinDefault             Original Verbs\n$brk"
 
#addr=`grep Address $codecfile | cut -f2 -d" "`

typeset -i nidnum=0

while read line;do
 
   chknode=`echo $line | grep "Node 0x" | cut -f2 -d" "`
   if [[ -n $chknode ]];then
      hexnode=$chknode
      vnode=`echo $hexnode | cut -f2 -d"x"` 
   fi

   pin=`echo $line | grep "Pin Default" | cut -f2 -d"x" | cut -f1 -d":"`

   if [[ -n $pin ]];then
       
      desc=`echo $line | cut -f2 -d"]"`
      jack=`grep -A8 "Node $hexnode" $codecfile | grep -A2 "$pin" | grep Color | cut -f2 -d"=" | cut -f1 -d","`
      color=`grep -A8 "Node $hexnode" $codecfile | grep -A2 "$pin" | grep Color | cut -f3 -d"="`
      
      # 71c Default Association/Sequence
      verb1=$codecaddr$vnode"71c"`echo $pin | cut -c7,8`

      # 71d Color/Misc 
      verb2=$codecaddr$vnode"71d"`echo $pin | cut -c5,6`
       
      # 71e Default Device/Connection Type
      verb3=$codecaddr$vnode"71e"`echo $pin | cut -c3,4`

      # 71f Port Connectivity/Location
      verb4=$codecaddr$vnode"71f"`echo $pin | cut -c1,2`

      printf "%7s %7s %-27s %3d %-6s %-12s %s %s %s %s\n" $jack $color "$desc" $hexnode $hexnode "0x"$pin $verb1 $verb2 $verb3 $verb4

      chkblklist="$jack $color $desc $hexnode 0x$pin"

      blklisted=0;i=0
      while [ $i -lt ${#blacklist[@]} ];do
         chk=`echo $chkblklist | grep "${blacklist[i]}"`
         if [[ $chk ]];then
            blklisted=1
         fi
         i=i+1
      done
         
      if [[ $blklisted = 0 ]];then
         vdesc[verbcount]="$desc"
         vjack[verbcount]=$jack
         vcolor[verbcount]=$color
         vhex[verbcount]=$hexnode
         vpin[verbcount]=$pin
         verbc[verbcount]=$verb1 
         verbd[verbcount]=$verb2 
         verbe[verbcount]=$verb3 
         verbf[verbcount]=$verb4
         verbcount=verbcount+1
      else
         blnodes=$blnodes$hexnode" "
      fi

   fi

done < $codecfile

echo -e "$brk\n"

# Show nodes that were blacklisted and removed
echo "Blacklist:" >> $debug
echo ${blacklist[*]} >> $debug
echo "Removed Nodes: $blnodes" >> $debug

# Correct Verbs

# Rules:
# Pin Defaults of 0x411111f0 or 0x400000f0 are removed 
# Remove CD at INT ATAPI
#     Taken Care of by blacklist array above, shouldn't be in current verb array
# 71c Sequence should always be 0
# 71c Association needs to be unique!
# 71d Set all Misc to 0 (Jack Detect Enabled) and determine which should be 1 later 
# 71e - Not Processed in this version 
# 71f Location should not use 02 for Front Panel, use 01 instead 

#
# Step 1 - Correct 71c Associations
#

echo "Checking 71c Associations" >> $debug
echo -e "\nCurrent Associations" >> $debug

i=0
while [ $i -lt $verbcount ]
do
    note=""
    assoc[i]=`echo ${verbc[i]} | cut -c7`
    if [[ ${assoc[i]} = 0 ]];then
       assoc[i]=1
       note=" note: Changed 0 to 1" 
    fi

    # Debug
    echo "${verbc[i]} = ${assoc[i]} $note" >> $debug

    i=i+1
done

# Determine unused association values
i=1;j=0
while (( i < 15 ));do 

   # convert to single hex digit 
   ihex=`printf "%x\n" $i`
   chk=`echo ${assoc[*]} | grep -w $ihex`

      if [[ -z $chk ]];then 
         unused[j]=$ihex
         j=j+1
      fi

   i=i+1

done

# Debug
echo -e "\n  Used associations = "${assoc[*]} >> $debug
echo "Unused associations = "${unused[*]} >> $debug
echo -e "\nCorrecting duplicate associations\n" >> $debug

i=0;nextassoc=0
while [ $i -lt $verbcount ]
do
    #build a assoc list without current node being checked 
    j=0;assoclist=""
    while [ $j -lt $verbcount ]
    do
        if [[ $j != $i ]];then
           assoclist=$assoclist${assoc[j]}" "
        fi
        j=j+1
    done

    echo "Checking if ${assoc[i]} already exists in: $assoclist" >> $debug

    chkassoc=`echo $assoclist | grep -w ${assoc[i]}`

    if [[ -n $chkassoc ]];then

       #There is a duplicate
       #Is this the first time we've seen this association?
       
       echo "   duplicate found - Is this the first time we've seen this association?" >> $debug
       firstassoc=`echo $newassoclist | grep -w ${assoc[i]}`

       if [[ -n $firstassoc ]];then 
          echo "   no - replacing association with: ${unused[nextassoc]}" >> $debug

          assoc[i]=${unused[nextassoc]} 
          nverbc[i]=`echo ${verbc[i]} | cut -c1-6`${assoc[i]}"0"
          nextassoc=nextassoc+1 

       else
          echo "   yes - ignoring" >> $debug

          nverbc[i]=`echo ${verbc[i]} | cut -c1-7`"0"

       fi

    else

       echo "   no duplicate found" >> $debug

       nverbc[i]=`echo ${verbc[i]} | cut -c1-7`"0"

    fi 

    newassoclist=$newassoclist${assoc[i]}" "
    i=i+1
    
done

echo -e "\nNew 71c Associations" >> $debug
echo " Before      After" >> $debug
echo "--------------------------------------------------" >> $debug

i=0
while [ $i -lt $verbcount ]
do
    echo ${verbc[i]}"   "${nverbc[i]}" "${verbd[i]}" "${verbe[i]}" "${verbf[i]} >> $debug
    i=i+1
done

#
# Step 2 - Correcting 71d Misc
#

echo -e "\nReset 71d Misc to 0" >> $debug

i=0
while [ $i -lt $verbcount ]
do
   nverbd[i]=`echo ${verbd[i]} | cut -c1-7`"0"
   #verbd[i]=$verb$b
   i=i+1
done
   

echo -e "New 71d Associations" >> $debug
echo " Before                After" >> $debug
echo "--------------------------------------------------" >> $debug
i=0
while [ $i -lt $verbcount ]
do
    echo ${verbd[i]}"   "${nverbc[i]}"  "${nverbd[i]}" "${verbe[i]}" "${verbf[i]} >> $debug
    i=i+1
done

#
# Step 3 - Correct 71e 
#

# Removed for now 
 
# 
# Step 4 - Correct 71f
#

echo -e "\nCorrect 71f 02 FP to 01" >> $debug

i=0
while [ $i -lt $verbcount ]
do
   verb=`echo ${verbf[i]} | cut -c1-7`
   misc=`echo ${verbf[i]} | cut -c8 | tr [a-z] [A-Z]`

   if [[ $misc = "2" ]];then
      misc="1"
   fi

   if [[ $misc != "1" ]];then
      misc="0"
   fi

   nverbf[i]=$verb$misc

   i=i+1

done

echo -e "New 71f Associations" >> $debug
echo " Before                                    After" >> $debug
echo "--------------------------------------------------" >> $debug
i=0
while [ $i -lt $verbcount ]
do
    echo ${verbd[i]}"   "${nverbc[i]}"  "${nverbd[i]}" "${verbe[i]}"  "${nverbf[i]} >> $debug
    i=i+1
done
echo " " >> $debug


#
# Step 5 - Show new verbs
#

echo -e "\n   Jack   Color  Description                  Node     PinDefault             Modified Verbs\n$brk"
i=0
while [ $i -lt $verbcount ]
do
    printf "%7s %7s %-27s %3d %-6s %-12s %s %s %s %s\n" ${vjack[i]} ${vcolor[i]} "${vdesc[i]}" ${vhex[i]} ${vhex[i]} "0x"${vpin[i]} ${nverbc[i]} ${nverbd[i]} ${verbe[i]} ${nverbf[i]}
    i=i+1
done

echo -e "$brk\n"

# verbs in one line

printf "Modified Verbs in One Line:"
i=0
while [ $i -lt $verbcount ]
do
    printf " %s %s %s %s" ${nverbc[i]} ${nverbd[i]} ${verbe[i]} ${nverbf[i]}
    i=i+1
done

echo -e "\n$brk\n"

