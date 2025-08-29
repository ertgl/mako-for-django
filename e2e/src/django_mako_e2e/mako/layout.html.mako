<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title><%block name="title">E2E | Mako for Django</%block></title>
</head>
<body>
  <header>
    <%block name="header__inner">
      <h1>Mako for Django - E2E</h1>
    </%block>
  </header>

  <%block name="aside" />

  <hr />

  ${ next.body() }
</body>
</html>
