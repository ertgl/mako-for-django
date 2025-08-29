<%inherit file="/samples/layouts/catalog.html.mako" />

<%namespace name="card_components" file="/samples/components/clsx-integration/card.html.mako" />

<%block name="title">
  CLSX Integration | ${ parent.title() }
</%block>

<%
  EDIT_IDX_RAW = request.GET.get("edit", "")
  EDIT_IDX = int(EDIT_IDX_RAW) if EDIT_IDX_RAW.isdigit() else None

  EDIT_MODE = EDIT_IDX is not None
%>

<table border="1" style="margin: 1em 0em; border: 1px solid grey;">
  <tbody>
    <tr>
      <th align="left">Edit mode:</th>
      <td align="left">${ EDIT_MODE }</td>
    </tr>
    <tr>
      <th align="left">Editable post index:</th>
      <td align="left">${ EDIT_IDX }</td>
    </tr>
  </tbody>
</table>

<div style="display: flex; flex-direction: column; gap: 1em">
  % for post_idx, post in enumerate(posts):
  <%
    is_post_editable = post_idx == EDIT_IDX

    post_html_id = f"post-{str(post_idx + 1)}"
  %>
  <div>
    <%card_components:card id="${ post_html_id }" class_name="card--custom" editable="${ is_post_editable }">
      <%def name="title()">
        <h3>${ post.title }</h3>
      </%def>

      <%def name="content()">
        ${ post.body }
      </%def>

      <div>
        <form action="${ f'#{post_html_id}' }">
          <input type="hidden" name="edit" value="${ '' if is_post_editable else str(post_idx) }" />

          <button type="submit">
            % if is_post_editable:
            Cancel
            % else:
            Edit
            % endif
          </button>
        </form>
      </div>
    </%card_components:card>
  </div>
  % endfor
</div>
