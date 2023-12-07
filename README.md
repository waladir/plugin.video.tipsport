<h1>Tipsport.cz</h1>
<p>
<h3>Kodi doplňek pro Tipsport.cz</h3>
<p>
<h4>Doplněk je funkční v Kodi běžícím ve Windows a Linuxu s Intel/AMD procesory a je třeba mít nainstalovaný Google Chrome. Na ostatních zařízení s jiným OS nebo ARMovým procesorem je možné použít docker kontejner (funguje v CoreELEC/LibreELEC). Bohužel pro Android neexistují ani potřebný driver ani nativní možnost spuštění dockeru. Doplněk tam tedy nebude fungovat.</h4><br>

<h3>Postup instalace</h3><br>
Stáhněte a nainstalujte <a href="https://codeload.github.com/waladir/script.module.selenium/zip/refs/heads/master">doplněk selenium</a> a samotný <a href="https://codeload.github.com/waladir/plugin.video.tipsport/zip/refs/heads/master">Tipsport.cz</a>

<h4>CoreELEC/LibreELEC</h4>
Pokud chcete provozovat doplněk v CoreELEC/LibreELEC, kde Google Chrome nejde standardně nainstalovat, nainstalujte si z nejprve z repozitáře CoreELEC/LibreELEC docker. Připojte se přes ssh a vytvořte a nastartujte container (cca. 1.3 GB!):

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

v1.0.0 (6.12.2023)<br>
- první verze<br><br>
</p>
