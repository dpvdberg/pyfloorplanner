from lark import Lark

from parser.YALParser import YALParser

y = YALParser()
fp = y.parse(open('datasets/MCNC/ami33.yal', 'r').read())

fp.align_horizontally()
fp.plot(draw_names=True)
