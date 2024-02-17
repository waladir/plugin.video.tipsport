<h1>Tipsport.cz</h1>
<p>
<h3>Kodi doplněk pro Tipsport.cz</h3>
<p>
Doplněk je funkční v Kodi běžícím ve Windows a Linuxu s Intel/AMD procesorem a vyžaduje mít nainstalovaný Google Chrome. Na ostatních zařízení s jiným OS nebo ARMovým procesorem je možné použít docker kontejner se Selenium Grid (funguje v CoreELEC/LibreELEC) nebo samostatně běžící Selenium Grid. Bohužel pro Android neexistují ani potřebný driver ani nativní možnost spuštění dockeru. Je možné využít vzdáleně běžící docker, ale toto řešení doporučuju jen v případě, že víte co děláte.<br>

<h3>Postup instalace</h3><br>
Stáhněte a nainstalujte <a href="https://codeload.github.com/waladir/script.module.selenium/zip/refs/heads/master">doplněk selenium</a> a samotný <a href="https://codeload.github.com/waladir/plugin.video.tipsport/zip/refs/heads/master">Tipsport.cz</a>

<h4>CoreELEC/LibreELEC</h4>
Pokud chcete provozovat doplněk v CoreELEC/LibreELEC, kde Google Chrome nejde standardně nainstalovat, nainstalujte si z nejprve z repozitáře CoreELEC/LibreELEC docker. Připojte se přes ssh (<a href="https://wiki.coreelec.org/coreelec:ssh">postup CoreELEC</a>) a vytvořte a nastartujte container (cca. 1.3 GB!):

<pre>
docker create \
   --name=selenium-chrome \
   -e TZ=Europe/Prague \
   -p 4444:4444 \
   -p 7900:7900 \
   --shm-size="1g" \
   --restart unless-stopped \
   --privileged \
   seleniarm/standalone-chromium:latest

docker start selenium-chrome
</pre><br>

V nastavení doplňku vyplňte jako Prohlížeč docker.<br><br>

<h4>Java</h4>
Selenium Grid lze pustit i na jiném počítači a doplněk k němu může přistupovat vzdáleně. Je potřeba mít nainstalované Java JRE a vyšší a Google Chrome.<br>

- stáhněte si aktuální verzi Selenium Serveru (selenium-server-<verze>.jar) z https://github.com/SeleniumHQ/selenium/releases/latest<br>
- spusťte Selenium Grid:<br>
 
<pre>java -jar selenium-server-<verze>.jar standalone --selenium-manager true</pre>
- v nastavení doplňku vyberte v Prohlížeč Selenium Grid a v Selenium Grid URL http://<adresa nebo jméno počítače s běžícím Selenium Grid>:4444/wd/hub<br><br>

<h4>Zadáním JSESSIONID přes webový formulář</h4>
Tento způsob nahrazuje přihlášení a při jeho použití není třeba volání žádného prohlížeče z doplňku.<br>

- v nastavení dopňku vyberte v Prohlížeč zadání přes web<br>
- v prohlížeči otevřete stránku z formulářem pro zadání JSESSIONID - http://&lt;adresa stroje s Kodi&gt;:8089/<br>
- na stránce zadejte podle postupu hodnotu JSESSIONID<br><br>

<hr>
v1.1.3 (17.2.2024)<br>
- přidaná možnost exportu JSESSIONID do souboru a jeho načtení<br>
- automatická obnova sessiony se nespouští při použití lokálního Google Chrome nebo Selenium Grid<br><br>

v1.1.2 (22.12.2023)<br>
- přidáná informace o průběhu zápasu/skóre<br><br>

v1.1.1 (16.12.2023)<br>
- oprava přihlášení přes JSESSIONID u Tipsport.sk<br><br>

v1.1.0 (13.12.2023)<br>
- možnost nahradit příhlášení  k Tipsportu zadáním hodnoty JSESSIONID přes webový formulář<br><br>

v1.0.5 (13.12.2023)<br>
- přidání služby, která prodlužuje platnost sessiony<br>
- úprava logování<br><br>
</p>
