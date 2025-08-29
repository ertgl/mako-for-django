<%inherit file="/samples/layouts/catalog.html.mako" />
<%namespace name="button" file="/samples/components/readme/button.html.mako" />

<%block name="title">
  README | ${ parent.title() }
</%block>

<%button:icon_button class_name="sample-button">
  ➖
</%button:icon_button>

<%button:icon_button class_name="sample-button" round="${ True }">
  ➕
</%button:icon_button>

<%button:basic_button class_name="sample-button">
  <%def name="icon()">✖️</%def>
  <%def name="label()">Cancel</%def>
</%button:basic_button>

<%button:basic_button class_name="sample-button" rounded="${ True }">
  <%def name="icon()">⚡</%def>
  <%def name="label()">Trigger</%def>
</%button:basic_button>
