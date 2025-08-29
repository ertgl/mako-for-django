<%namespace name="component" file="/samples/components/component-system/component.html.mako" />

<%def name="base(attrs=None, icon=None, label=None, **kwargs)">
  <%
    if attrs:
      attrs = {}
    kwargs["attrs"] = [
      "data-interactive",
      ("class", clsx(["button", attrs.pop("class", None)])),
      attrs,
    ]
  %>

<%call expr="component.base('button', **kwargs)">
    % if icon:
      <div class="button__icon">
        ${ icon() }
      </div>
    % endif
    % if label:
      <div class="button__label">
        ${ label() }
      </div>
    % endif
  </%call>
</%def>

<%def name="button(**kwargs)">
  ${ self.base(
      icon=getattr(caller, "icon", None),
      label=getattr(caller, "label", None),
      **kwargs
    ) }
</%def>
