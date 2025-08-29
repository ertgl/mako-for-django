<%inherit file="/layout.html.mako" />

<%block name="title">
  Samples | ${ parent.title() }
</%block>

<%block name="header__inner">
    ${ parent.header__inner() }

    <a href="${ reverse_url('samples:index') }">
      <h2>Samples</h2>
    </a>
</%block>

<%block name="aside">
  <aside>
    <ul>
      <li>
        <a href="${ reverse_url('samples:clsx-integration') }">
          <b>CLSX integration</b>
        </a>
      </li>
      <li>
        <a href="${ reverse_url('samples:component-system') }">
          <b>Component system</b>
        </a>
      </li>
      <li>
        Partial rendering

        <ul>
          <li>
            <a href="${ reverse_url('samples:class-based-partial-rendering') }">
              <b>Class-based view</b>
            </a>
          </li>
          <li>
            <a href="${ reverse_url('samples:functional-partial-rendering') }">
              <b>Functional view</b>
            </a>
          </li>
        </ul>
      </li>
      <li>
        <a href="${ reverse_url('samples:readme') }">
          <b>README</b>
        </a>
      </li>
    </ul>
  </aside>
</%block>

${ next.body() }
