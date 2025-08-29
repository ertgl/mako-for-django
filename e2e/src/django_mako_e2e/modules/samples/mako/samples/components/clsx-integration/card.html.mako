<%def name="card(class_name=None, editable=False, **rest)">
  <div
    class="${ clsx(['card', ('card--editable', editable), class_name]) }"
    style="display: flex; flex-direction: column; gap: 0.25em; padding: 10px 15px; border: 1px grey solid; border-radius: 8px;"
    % for k, v in rest.items():
      ${ k | h }="${ v }"
    % endfor
  >
    % if caller.title:
      <div
        class="card__title"
        % if editable:
        contenteditable="true"
        style="padding: 0px 10px; border: 1px dashed grey"
        % endif
      >
        ${ caller.title() }
      </div>
    % endif

    % if caller.content:
      <div
        class="card__content"
        % if editable:
        contenteditable="true"
        style="padding: 20px 10px; border: 1px dashed grey"
        % endif
      >
        ${ caller.content() }
      </div>
    % endif

    ${ caller.body() }
  </div>
</%def>
