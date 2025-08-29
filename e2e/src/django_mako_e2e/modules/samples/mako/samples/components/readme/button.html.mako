<%def
  name="base_button(
    class_name=None,
    icon=None,
    label=None,
    round=False,
    rounded=False,
  )"
>
  <button
    class="${ clsx([
      'button',
      ('button--round', round),
      ('button--rounded', rounded),
      class_name,
    ]) }"
  >
    % if icon:
      <span class="button__icon">
        ${ icon() }
      </span>
    % endif
    % if label:
      <span class="button__label">
        ${ label() }
      </span>
    % endif
  </button>
</%def>

<%def name="basic_button(class_name=None, rounded=False)">
  <%self:base_button
    class_name="${ ['button--basic', class_name] }"
    icon="${ getattr(caller, 'icon', None) }"
    label="${ getattr(caller, 'label', None) }"
    rounded="${ rounded }"
  />
</%def>

<%def name="icon_button(class_name=None, round=False)">
  <%self:base_button
    class_name="${ ['button--icon', class_name] }"
    icon="${ getattr(caller, 'body', None) }"
    round="${ round }"
  />
</%def>
