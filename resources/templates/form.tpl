<html>
  <head>
      <title>Vložení JSESSIONID do doplňku Tipsport.cz</title>
  </head>
  <body>
    <h2><font color="red">{{ message }}</font></h2>
    <form method="post" action="/">
            Zadejte JSESSIONID: <input name="jsessionid" size="50"><br><br>
            <input type="submit" value="Uložit">
    </form>
    <p>Uvedený postup platí pro Google Chrome, ale i v ostatních prohlížečích (Edge, Firefox, ...) je stejný nebo jen s minimálními odlištnostmi.<br>
    <ul>
       <li>V prohlížeči otevřete stránku Tipsportu a pokud jste přihlášení, odhlašte se.</li>
       <li>Stiskněte klávasu F12, spustí se vývojařská konzole. Doporučuju vpravo nahoře kliknout na svislé tři tečky a vybrat ukotvení dolů.</li>
       <li>Překlikněte na záložku Síť.</li>
       <li>Na webu Tipsportu se standardně přihlašte.</li>
       <li>Vlevo nahoře do políčka pro filtrování napište "session".</li>
       <li>Klikněte na vyfiltrovaný požadavek a vpravo vyberte záložku Cookies.</li>
       <li>V <b>Cookies odpovědí/vrácených cookies</b> (pozor, ne odelsaných!) vyberte <b>celou</b> hodnotu u JSESSIONID a zkopírujte ji do schránky.</li>
       <li>Vývojářskou konzoli dalším stiskem klávesy F12 zavřete a můžete zavřít i stránku Tipsportu.</li>
       <li>Hodnotu JSESSIONID vložte do formuláře na stránce a klikněte na tlačítko Uložit. Stránku můžete zavřít.</li>
    </ul>
    <center><img src="/img/screen.jpg"></center>
  </body>
</html>
