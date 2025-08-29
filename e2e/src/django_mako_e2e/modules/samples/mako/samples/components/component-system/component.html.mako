<%namespace name="element" file="/samples/components/component-system/element.html.mako" />

<%def name="base(tag, attrs=None)">
  <${ tag }${ " " if attrs else '' }${ element.attributes(attrs) }>
    ${ caller.body() }
  </${ tag }>
</%def>