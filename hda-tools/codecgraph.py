#!/usr/bin/python
#
# Script to generate graphviz graphs from HDA-Intel codec information
#
# by Eduardo Habkost <ehabkost@mandriva.com>
#
# Copyright (c) 2006,2007 Eduardo Habkost <ehabkost@mandriva.com>
# Copyright (c) 2006,2007 Mandriva Conectiva
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import re, sys

ALL_NODES = False

def indentlevel(line):
	"""Return the indent level of a line"""
	m = re_indent.match(line)
	if not m:
		return 0
	return len(m.group(0))

def parse_item(level, lines):
	"""Read a line and corresponding indented lines"""
	item = lines.pop(0).rstrip(' \r\n').lstrip(' ')
	subitems = list(parse_items(level, lines))
	return item,subitems

def parse_items(level, lines):
	"""Parse a list of indented lines"""
	while lines:
		l = lines[0]
		linelvl = indentlevel(l)
		if linelvl <= level:
			# end of list
			break
		yield parse_item(linelvl, lines)

def coloravg(a, b, v):
	r = tuple([int(a[i]*(1-v) + b[i]*v) for i in 0,1,2])
	return r

def formatcolor(c):
	return '#%02x%02x%02x' % c

class Amplifier:
	def __init__(self, ofs, nsteps, stepsize, mute):
		self.ofs = int(ofs, 16)
		self.nsteps = int(nsteps, 16)
		self.stepsize = stepsize
		self.mute = mute

	def set_values(self, values):
		self.values = values
		self.gainvalues = [v & 0x7f for v in values]
		self.mutevalues = [(v & 0x80) <> 0 for v in values]

	def color(self):
		if True in self.mutevalues:
			level = 0
		else:
			average = sum(self.gainvalues)/len(self.gainvalues)

			if self.nsteps == 0:
				level = 1
			else:
				#XXX: confirm if this formula is correct
				level = 1-float(average-self.ofs)/(self.nsteps)

		if level < 0: level = 0
		if level > 1: level = 1

		zerocolor = (200, 200, 200)
		fullcolor = (0, 0, 255)
		color = coloravg(zerocolor, fullcolor, level)

		return formatcolor(color)

class Node:
	node_info_re = re.compile('^Node (0x[0-9a-f]*) \[(.*?)\] wcaps 0x[0-9a-f]*?: (.*)$')
	final_hex_re = re.compile(' *(0x[0-9a-f]*)$')

	def __init__(self, codec, item, subitems):
		self.item = item
		self.subitems = subitems
		self.codec = codec

		fields = {}

		# split first line and get some fields
		data = item.split(' ')
		m = self.node_info_re.match(item)
		self.nid = int(m.group(1), 16)
		self.type = m.group(2)
		wcapstr = m.group(3)

		self.wcaps = wcapstr.split()

		# parse all items on the node information
		for item,subitems in self.subitems:
			# Parse node fields
			if ':' in item:
				f,v = item.split(':', 1)
				v = v.lstrip()

				# strip hex number at the end.
				# some fields, such as Pincap & Pin Default,
				# have an hex number in the end
				m = self.final_hex_re.search(f)
				if m:
					f = self.final_hex_re.sub('', f)

					# store the hex value and the
					# string, on different keys
					fields[f+'-hex'] = m.group(1),subitems
					fields[f] = v,subitems
				else:
					fields[f] = v,subitems
			else:
				sys.stderr.write("Unknown node item: %s\n" % (item))

		self.fields = fields

		# parse connection info
		conn = fields.get('Connection', ('0', []))

		number,items = conn
		self.num_inputs = int(number)
		conns = []
		self.active_conn = None
		for i,sub in items:
			for j in i.split():
				active = j.endswith('*')
				j = j.rstrip('*')
				nid = int(j, 16)
				conns.append(nid)
				if active:
					self.active_conn = nid
		assert len(conns) == self.num_inputs
		self.inputs = conns

		if not self.active_conn and self.num_inputs == 1:
			self.active_conn = self.inputs[0]

		# parse amplifier info
		def parse_amps(name, count):
			capstr = fields['%s caps' % (name)][0]

			if capstr == 'N/A':
				capstr = 'ofs=0x00, nsteps=0x00, stepsize=0x00, mute=0'

			capl = capstr.split(', ')

			caps = {}
			for cap in capl:
				cname,cval = cap.split('=', 1)
				caps[cname] = cval

			valstr = fields['%s vals' % (name)][0]
			vals = re.findall(r'\[([^]]*)\]', valstr)

			# warn if Amp-In vals field is broken
			if count != len(vals):
				sys.stderr.write("Node 0x%02x: Amp-In vals count is wrong: values found: %d. expected: %d\n" % (self.nid, len(vals), count))

			amps = []
			for i in range(count):
				amp = Amplifier(caps['ofs'], caps['nsteps'],
			                        caps['stepsize'], caps['mute'])
				if len(vals) > i: intvals = [int(v, 16) for v in vals[i].split(' ')]
				# just in case the "vals" field is
				# broken in our input file
				else: intvals = [0, 0]
				amp.set_values(intvals)
				amps.append(amp)

			return amps

		inamps = self.num_inamps()
		if inamps > 0:
			self.inamps = parse_amps('Amp-In', inamps)
		if self.has_outamp():
			self.outamp, = parse_amps('Amp-Out', 1)

		self.outputs = []

	def new_output(self, nid):
		self.outputs.append(nid)

	def input_nodes(self):
		for c in self.inputs:
			yield self.codec.get_node(c)

	def is_divided(self):
		if self.type == 'Pin Complex':
			return True
		
		return False

	def idstring(self):
		return 'nid-%02x' % (self.nid)

	def has_outamp(self):
		return 'Amp-Out' in self.wcaps

	def outamp_id(self):
		return '"%s-ampout"' % (self.idstring())

	def out_id(self):
		if self.is_divided():
			return self.main_output_id()

		if self.has_outamp():
			return self.outamp_id()

		return self.outamp_next_id()

	def has_inamp(self):
		return 'Amp-In' in self.wcaps

	def many_ampins(self):
		types = ['Audio Mixer']
		return self.type in types

	def num_inamps(self):
		if not self.has_inamp(): return 0
		elif self.many_ampins(): return self.num_inputs
		else: return 1

	def inamp_id(self, orignid):
		if self.many_ampins():
			return '"%s-ampin-%s"' % (self.idstring(), orignid)
		return '"%s-ampin"' % (self.idstring())

	def in_id(self, orignid):
		if self.is_divided():
			return self.main_input_id()

		if self.has_inamp():
			return self.inamp_id(orignid)

		return self.inamp_next_id()

	def main_id(self):
		assert not self.is_divided()
		return '"%s"' % (self.idstring())

	def main_input_id(self):
		assert self.is_divided()
		return '"%s-in"' % (self.idstring())

	def main_output_id(self):
		assert self.is_divided()
		return '"%s-out"' % (self.idstring())

	def inamp_next_id(self):
		"""ID of the node where the In-Amp would be connected"""
		if self.is_divided():
			return self.main_output_id()

		return self.main_id()

	def outamp_next_id(self):
		"""ID of the node where the Out-Amp would be connected"""
		if self.is_divided():
			return self.main_input_id()

		return self.main_id()

	def wcaps_label(self):
		not_shown = ['Amp-In', 'Amp-Out']
		show = [cap for cap in self.wcaps if not cap in not_shown]
		return ' '.join(show)

	def label(self):
		r = '0x%02x' % (self.nid)
		print '// %r' % (self.fields)
		pdef = self.fields.get('Pin Default')
		if pdef:
			pdef,subdirs = pdef
			r += '\\n%s' % (pdef)

		r += '\\n%s' % (self.wcaps_label())

		pincap = self.fields.get('Pincap')
		if pincap:
			pincap,subdirs = pincap
			r += '\\n%s' % (pincap)

		r = '"%s"' % (r)
		return r

	def show_input(self):
		return ALL_NODES or len(self.inputs) > 0

	def show_output(self):
		return ALL_NODES or len(self.outputs) > 0

	def additional_attrs(self):
		default_attrs = [ ('shape', 'box'), ('color', 'black') ]
		shape_dict = {
			'Audio Input':[ ('color', 'red'),
			                ('shape', 'ellipse') ],
			'Audio Output':[ ('color', 'blue'),
			                 ('shape', 'ellipse') ],
			'Pin Complex':[ ('color', 'green'),
			                ('shape', 'box') ],
			'Audio Selector':[ ('shape', 'parallelogram'),
			                   ('orientation', '0')  ],
			'Audio Mixer':[ ('shape', 'hexagon') ],
			'Unknown Node':[ ('color', 'red'),
			                 ('shape', 'Mdiamond') ],
		}
		return shape_dict.get(self.type, default_attrs)

	def new_node(self, f, id, attrs):
		f.write(' %s ' % (id))
		if attrs:
			attrstr = ', '.join('%s=%s' % (f,v) for f,v in attrs)
			f.write('[%s]' % (attrstr))
		f.write('\n')

	def dump_main_input(self, f):
		if self.show_input():
			self.new_node(f, self.main_input_id(), self.get_attrs())

	def dump_main_output(self, f):
		if self.show_output():
			self.new_node(f, self.main_output_id(), self.get_attrs())

	def get_attrs(self):
		attrs = [ ('label', self.label()) ]
		attrs.extend(self.additional_attrs())
		return attrs

	def dump_main(self, f):
		if not self.is_divided():
			if self.show_input() or self.show_output():
				self.new_node(f, self.main_id(), self.get_attrs())
		else:
			self.dump_main_input()
			self.dump_main_output()

	def show_amp(self, f, id, type, frm, to, label='', color=None):
		if color is None: fill = ''
		else: fill=' color="%s"' % (color)

		f.write('  %s [label = "%s", shape=triangle orientation=-90%s];\n' % (id, label, fill))
		f.write('  %s -> %s [arrowsize=0.5, arrowtail=dot, weight=2.0%s];\n' % (frm, to, fill))

	def dump_out_amps(self, f):
		if self.show_output() and self.has_outamp():
			self.show_amp(f, self.outamp_id(), "Out", self.outamp_next_id(), self.outamp_id(), '', self.outamp.color())

	def dump_in_amps(self, f):
		if self.show_input() and self.has_inamp():

			if self.many_ampins():
				amporigins = [("%d (0x%02x)" % (n, self.inputs[n]), self.inputs[n]) for n in range(len(self.inputs))]
			else:
				amporigins = [ ('', None) ]

			for i in range(len(amporigins)):
				label,origin = amporigins[i]
				ampid = self.inamp_id(origin)
				self.show_amp(f, ampid, "In", ampid, self.inamp_next_id(), label, self.inamps[i].color())

	def dump_amps(self, f):
		self.dump_out_amps(f)
		self.dump_in_amps(f)

	def is_conn_active(self, c):
		if self.type == 'Audio Mixer':
			return True
		if c == self.active_conn:
			return True
		return False

	def dump_graph(self, f):
		codec = self.codec
		name = "cluster-%s" % (self.idstring())
		if self.is_divided():
			f.write('subgraph "%s-in" {\n' % (name))
			f.write('  pencolor="gray80"\n')
			self.dump_main_input(f)
			self.dump_out_amps(f)
			f.write('}\n')

			f.write('subgraph "%s-out" {\n' % (name))
			f.write('  pencolor="gray80"\n')
			self.dump_main_output(f)
			self.dump_in_amps(f)
			f.write('}\n')
		else: 
			f.write('subgraph "%s" {\n' % (name))
			f.write('  pencolor="gray80"\n')
			self.dump_main(f)
			self.dump_amps(f)
			f.write('}\n')

		for origin in self.input_nodes():
			if self.is_conn_active(origin.nid):
				attrs="[color=gray20]"
			else:
				attrs="[color=gray style=dashed]"
			f.write('%s -> %s %s;\n' % (origin.out_id(), self.in_id(origin.nid), attrs))
		

re_indent = re.compile("^ *")
 
class CodecInfo:
	def __init__(self, f):
		self.fields = {}
		self.nodes = {}
		lines = f.readlines()
		total_lines = len(lines)

		for item,subitems in parse_items(-1, lines):
			line = total_lines-len(lines)
			try:
				if not ': ' in item and item.endswith(':'):
					# special case where there is no ": "
					# but we want to treat it like a "key: value"
					# line
					# (e.g. "Default PCM:" line)
					item += ' '

				if item.startswith('Node '):
					n = Node(self, item, subitems)
					self.nodes[n.nid] = n
				if item.startswith('No Modem Function Group found'):
					# ignore those lines
					pass
				elif ': ' in item:
					f,v = item.split(': ', 1)
					self.fields[f] = v
				elif item.strip() == '':
					continue
				else:
					sys.stderr.write("Warning: line %d ignored: %s\n" % (line, item))
			except:
				sys.stderr.write('Exception around line %d\n' % (line))
				sys.stderr.write('item: %r\n' % (item))
				sys.stderr.write('subitems: %r\n' % (subitems))
				raise

		self.create_out_lists()

	def get_node(self, nid):
		n = self.nodes.get(nid)
		if not n:
			# create a fake node
			n = Node(self, 'Node 0x%02x [Unknown Node] wcaps 0x0000: ' % (nid), [])
			self.nodes[nid] = n
			n.label = lambda: ('"Unknown Node 0x%02x"' % (nid))
		return n

	def create_out_lists(self):
		for n in self.nodes.values():
			for i in n.input_nodes():
				i.new_output(n.nid)

	def dump(self):
		print "Codec: %s" % (self.fields['Codec'])
		print "Nodes: %d" % (len(self.nodes))
		for n in self.nodes.values():
			print "Node: 0x%02x" % (n.nid),
			print " %d conns" % (n.num_inputs)

	def dump_graph(self, f):
		f.write('digraph {\n')
		f.write("""rankdir=LR
		ranksep=3.0
		""")
		for n in self.nodes.values():
			n.dump_graph(f)
		f.write('}\n')

def main(argv):
	f = open(argv[1], 'r')
	ci = CodecInfo(f)
	ci.dump_graph(sys.stdout)

if __name__ == '__main__':
	main(sys.argv)
