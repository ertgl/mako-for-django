<%inherit file="/samples/layouts/catalog.html.mako" />

<%block name="title">
  Partial Rendering | ${ parent.title() }
</%block>

% if partial_template_uri:
<%include file="${ partial_template_uri }" />
% else:
  No content template specified.
% endif
