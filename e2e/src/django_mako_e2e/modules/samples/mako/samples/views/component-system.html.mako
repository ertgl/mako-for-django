<%inherit file="/samples/layouts/catalog.html.mako" />
<%namespace name="button" file="/samples/components/component-system/button.html.mako" />

<%block name="title">
  Component system | ${ parent.title() }
</%block>

<%button:button attrs="${ { 'aria-label': 'Click', 'class': 'sample-button' } }">
  <%def name="icon()">+</%def>
  <%def name="label()">Click</%def>
</%button:button>
