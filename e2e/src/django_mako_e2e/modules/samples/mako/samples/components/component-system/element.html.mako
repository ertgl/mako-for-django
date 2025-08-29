<%def name="attributes(attrs)">\
% if attrs:
% for attr in (attrs.items() if isinstance(attrs, dict) else attrs):
% if isinstance(attr, tuple) and len(attr) == 2:
% if attr[0]:
${ attr[0] | h }="${ attr[1] | h }"${ '' if loop.last else ' ' }\
% endif
% elif isinstance(attr, (list, tuple, dict)):
${ self.attributes(attr) }${ '' if loop.last else ' ' }\
% elif attr is not None:
${ attr | h }${ '' if loop.last else ' ' }\
% endif
% endfor
% endif
</%def>