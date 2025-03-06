import os
import pyperclip

def generate_tree(directory, prefix="", tree_str=""):
    ignore_list = {"__pycache__", ".vscode", ".gitignore", ".git", ".prettierrc", "auto-py-to-exe.json", "build.json", "Dispo.pdf", "humans.py", "main_old.py", "template.jpeg", "tree_maker.py"}  # Folders and files to ignore
    entries = sorted(os.listdir(directory), key=lambda e: (os.path.isdir(os.path.join(directory, e)), e.lower()))
    entries = [e for e in entries if e not in ignore_list]  # Filter out ignored entries
    for i, entry in enumerate(entries):
        path = os.path.join(directory, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += prefix + connector + entry + "\n"
        if os.path.isdir(path):
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_str = generate_tree(path, new_prefix, tree_str)
    return tree_str

if __name__ == "__main__":
    project_dir = os.path.abspath("./output/Time Clicker")  # Change this to your project's root directory if needed
    tree_structure = os.path.basename(project_dir) + "/\n"
    tree_structure += generate_tree(project_dir)
    print(tree_structure)
    pyperclip.copy(tree_structure)
    print("Directory tree copied to clipboard.")


'''
TREE FOR CURRENT PROJECT AFTER USING PYINSTALLER


Time Clicker/
├── Time Clicker.exe
└── _internal
    ├── _asyncio.pyd
    ├── _bz2.pyd
    ├── _ctypes.pyd
    ├── _decimal.pyd
    ├── _hashlib.pyd
    ├── _lzma.pyd
    ├── _multiprocessing.pyd
    ├── _overlapped.pyd
    ├── _queue.pyd
    ├── _socket.pyd
    ├── _ssl.pyd
    ├── _tkinter.pyd
    ├── _wmi.pyd
    ├── api-ms-win-core-console-l1-1-0.dll
    ├── api-ms-win-core-datetime-l1-1-0.dll
    ├── api-ms-win-core-debug-l1-1-0.dll
    ├── api-ms-win-core-errorhandling-l1-1-0.dll
    ├── api-ms-win-core-file-l1-1-0.dll
    ├── api-ms-win-core-file-l1-2-0.dll
    ├── api-ms-win-core-file-l2-1-0.dll
    ├── api-ms-win-core-handle-l1-1-0.dll
    ├── api-ms-win-core-heap-l1-1-0.dll
    ├── api-ms-win-core-interlocked-l1-1-0.dll
    ├── api-ms-win-core-libraryloader-l1-1-0.dll
    ├── api-ms-win-core-localization-l1-2-0.dll
    ├── api-ms-win-core-memory-l1-1-0.dll
    ├── api-ms-win-core-namedpipe-l1-1-0.dll
    ├── api-ms-win-core-processenvironment-l1-1-0.dll
    ├── api-ms-win-core-processthreads-l1-1-0.dll
    ├── api-ms-win-core-processthreads-l1-1-1.dll
    ├── api-ms-win-core-profile-l1-1-0.dll
    ├── api-ms-win-core-rtlsupport-l1-1-0.dll
    ├── api-ms-win-core-string-l1-1-0.dll
    ├── api-ms-win-core-synch-l1-1-0.dll
    ├── api-ms-win-core-synch-l1-2-0.dll
    ├── api-ms-win-core-sysinfo-l1-1-0.dll
    ├── api-ms-win-core-timezone-l1-1-0.dll
    ├── api-ms-win-core-util-l1-1-0.dll
    ├── api-ms-win-crt-conio-l1-1-0.dll
    ├── api-ms-win-crt-convert-l1-1-0.dll
    ├── api-ms-win-crt-environment-l1-1-0.dll
    ├── api-ms-win-crt-filesystem-l1-1-0.dll
    ├── api-ms-win-crt-heap-l1-1-0.dll
    ├── api-ms-win-crt-locale-l1-1-0.dll
    ├── api-ms-win-crt-math-l1-1-0.dll
    ├── api-ms-win-crt-private-l1-1-0.dll
    ├── api-ms-win-crt-process-l1-1-0.dll
    ├── api-ms-win-crt-runtime-l1-1-0.dll
    ├── api-ms-win-crt-stdio-l1-1-0.dll
    ├── api-ms-win-crt-string-l1-1-0.dll
    ├── api-ms-win-crt-time-l1-1-0.dll
    ├── api-ms-win-crt-utility-l1-1-0.dll
    ├── base_library.zip
    ├── buildings.py
    ├── Buttons.py
    ├── data.py
    ├── freetype.dll
    ├── libcrypto-3.dll
    ├── libffi-8.dll
    ├── libjpeg-9.dll
    ├── libmodplug-1.dll
    ├── libogg-0.dll
    ├── libopus-0.dll
    ├── libopusfile-0.dll
    ├── libpng16-16.dll
    ├── libssl-3.dll
    ├── libtiff-5.dll
    ├── libwebp-7.dll
    ├── Logger.py
    ├── MSVCR100.dll
    ├── portmidi.dll
    ├── pyexpat.pyd
    ├── python3.dll
    ├── python312.dll
    ├── SDL2.dll
    ├── SDL2_image.dll
    ├── SDL2_mixer.dll
    ├── SDL2_ttf.dll
    ├── select.pyd
    ├── tcl86t.dll
    ├── tk86t.dll
    ├── ucrtbase.dll
    ├── unicodedata.pyd
    ├── utils.py
    ├── VCRUNTIME140.dll
    ├── VCRUNTIME140_1.dll
    ├── zlib1.dll
    ├── _tcl_data
    │   ├── auto.tcl
    │   ├── clock.tcl
    │   ├── history.tcl
    │   ├── init.tcl
    │   ├── package.tcl
    │   ├── parray.tcl
    │   ├── safe.tcl
    │   ├── tclIndex
    │   ├── tm.tcl
    │   ├── word.tcl
    │   ├── encoding
    │   │   ├── ascii.enc
    │   │   ├── big5.enc
    │   │   ├── cns11643.enc
    │   │   ├── cp1250.enc
    │   │   ├── cp1251.enc
    │   │   ├── cp1252.enc
    │   │   ├── cp1253.enc
    │   │   ├── cp1254.enc
    │   │   ├── cp1255.enc
    │   │   ├── cp1256.enc
    │   │   ├── cp1257.enc
    │   │   ├── cp1258.enc
    │   │   ├── cp437.enc
    │   │   ├── cp737.enc
    │   │   ├── cp775.enc
    │   │   ├── cp850.enc
    │   │   ├── cp852.enc
    │   │   ├── cp855.enc
    │   │   ├── cp857.enc
    │   │   ├── cp860.enc
    │   │   ├── cp861.enc
    │   │   ├── cp862.enc
    │   │   ├── cp863.enc
    │   │   ├── cp864.enc
    │   │   ├── cp865.enc
    │   │   ├── cp866.enc
    │   │   ├── cp869.enc
    │   │   ├── cp874.enc
    │   │   ├── cp932.enc
    │   │   ├── cp936.enc
    │   │   ├── cp949.enc
    │   │   ├── cp950.enc
    │   │   ├── dingbats.enc
    │   │   ├── ebcdic.enc
    │   │   ├── euc-cn.enc
    │   │   ├── euc-jp.enc
    │   │   ├── euc-kr.enc
    │   │   ├── gb12345.enc
    │   │   ├── gb1988.enc
    │   │   ├── gb2312-raw.enc
    │   │   ├── gb2312.enc
    │   │   ├── iso2022-jp.enc
    │   │   ├── iso2022-kr.enc
    │   │   ├── iso2022.enc
    │   │   ├── iso8859-1.enc
    │   │   ├── iso8859-10.enc
    │   │   ├── iso8859-11.enc
    │   │   ├── iso8859-13.enc
    │   │   ├── iso8859-14.enc
    │   │   ├── iso8859-15.enc
    │   │   ├── iso8859-16.enc
    │   │   ├── iso8859-2.enc
    │   │   ├── iso8859-3.enc
    │   │   ├── iso8859-4.enc
    │   │   ├── iso8859-5.enc
    │   │   ├── iso8859-6.enc
    │   │   ├── iso8859-7.enc
    │   │   ├── iso8859-8.enc
    │   │   ├── iso8859-9.enc
    │   │   ├── jis0201.enc
    │   │   ├── jis0208.enc
    │   │   ├── jis0212.enc
    │   │   ├── koi8-r.enc
    │   │   ├── koi8-u.enc
    │   │   ├── ksc5601.enc
    │   │   ├── macCentEuro.enc
    │   │   ├── macCroatian.enc
    │   │   ├── macCyrillic.enc
    │   │   ├── macDingbats.enc
    │   │   ├── macGreek.enc
    │   │   ├── macIceland.enc
    │   │   ├── macJapan.enc
    │   │   ├── macRoman.enc
    │   │   ├── macRomania.enc
    │   │   ├── macThai.enc
    │   │   ├── macTurkish.enc
    │   │   ├── macUkraine.enc
    │   │   ├── shiftjis.enc
    │   │   ├── symbol.enc
    │   │   └── tis-620.enc
    │   ├── http1.0
    │   │   ├── http.tcl
    │   │   └── pkgIndex.tcl
    │   ├── msgs
    │   │   ├── af.msg
    │   │   ├── af_za.msg
    │   │   ├── ar.msg
    │   │   ├── ar_in.msg
    │   │   ├── ar_jo.msg
    │   │   ├── ar_lb.msg
    │   │   ├── ar_sy.msg
    │   │   ├── be.msg
    │   │   ├── bg.msg
    │   │   ├── bn.msg
    │   │   ├── bn_in.msg
    │   │   ├── ca.msg
    │   │   ├── cs.msg
    │   │   ├── da.msg
    │   │   ├── de.msg
    │   │   ├── de_at.msg
    │   │   ├── de_be.msg
    │   │   ├── el.msg
    │   │   ├── en_au.msg
    │   │   ├── en_be.msg
    │   │   ├── en_bw.msg
    │   │   ├── en_ca.msg
    │   │   ├── en_gb.msg
    │   │   ├── en_hk.msg
    │   │   ├── en_ie.msg
    │   │   ├── en_in.msg
    │   │   ├── en_nz.msg
    │   │   ├── en_ph.msg
    │   │   ├── en_sg.msg
    │   │   ├── en_za.msg
    │   │   ├── en_zw.msg
    │   │   ├── eo.msg
    │   │   ├── es.msg
    │   │   ├── es_ar.msg
    │   │   ├── es_bo.msg
    │   │   ├── es_cl.msg
    │   │   ├── es_co.msg
    │   │   ├── es_cr.msg
    │   │   ├── es_do.msg
    │   │   ├── es_ec.msg
    │   │   ├── es_gt.msg
    │   │   ├── es_hn.msg
    │   │   ├── es_mx.msg
    │   │   ├── es_ni.msg
    │   │   ├── es_pa.msg
    │   │   ├── es_pe.msg
    │   │   ├── es_pr.msg
    │   │   ├── es_py.msg
    │   │   ├── es_sv.msg
    │   │   ├── es_uy.msg
    │   │   ├── es_ve.msg
    │   │   ├── et.msg
    │   │   ├── eu.msg
    │   │   ├── eu_es.msg
    │   │   ├── fa.msg
    │   │   ├── fa_in.msg
    │   │   ├── fa_ir.msg
    │   │   ├── fi.msg
    │   │   ├── fo.msg
    │   │   ├── fo_fo.msg
    │   │   ├── fr.msg
    │   │   ├── fr_be.msg
    │   │   ├── fr_ca.msg
    │   │   ├── fr_ch.msg
    │   │   ├── ga.msg
    │   │   ├── ga_ie.msg
    │   │   ├── gl.msg
    │   │   ├── gl_es.msg
    │   │   ├── gv.msg
    │   │   ├── gv_gb.msg
    │   │   ├── he.msg
    │   │   ├── hi.msg
    │   │   ├── hi_in.msg
    │   │   ├── hr.msg
    │   │   ├── hu.msg
    │   │   ├── id.msg
    │   │   ├── id_id.msg
    │   │   ├── is.msg
    │   │   ├── it.msg
    │   │   ├── it_ch.msg
    │   │   ├── ja.msg
    │   │   ├── kl.msg
    │   │   ├── kl_gl.msg
    │   │   ├── ko.msg
    │   │   ├── ko_kr.msg
    │   │   ├── kok.msg
    │   │   ├── kok_in.msg
    │   │   ├── kw.msg
    │   │   ├── kw_gb.msg
    │   │   ├── lt.msg
    │   │   ├── lv.msg
    │   │   ├── mk.msg
    │   │   ├── mr.msg
    │   │   ├── mr_in.msg
    │   │   ├── ms.msg
    │   │   ├── ms_my.msg
    │   │   ├── mt.msg
    │   │   ├── nb.msg
    │   │   ├── nl.msg
    │   │   ├── nl_be.msg
    │   │   ├── nn.msg
    │   │   ├── pl.msg
    │   │   ├── pt.msg
    │   │   ├── pt_br.msg
    │   │   ├── ro.msg
    │   │   ├── ru.msg
    │   │   ├── ru_ua.msg
    │   │   ├── sh.msg
    │   │   ├── sk.msg
    │   │   ├── sl.msg
    │   │   ├── sq.msg
    │   │   ├── sr.msg
    │   │   ├── sv.msg
    │   │   ├── sw.msg
    │   │   ├── ta.msg
    │   │   ├── ta_in.msg
    │   │   ├── te.msg
    │   │   ├── te_in.msg
    │   │   ├── th.msg
    │   │   ├── tr.msg
    │   │   ├── uk.msg
    │   │   ├── vi.msg
    │   │   ├── zh.msg
    │   │   ├── zh_cn.msg
    │   │   ├── zh_hk.msg
    │   │   ├── zh_sg.msg
    │   │   └── zh_tw.msg
    │   ├── opt0.4
    │   │   ├── optparse.tcl
    │   │   └── pkgIndex.tcl
    │   └── tzdata
    │       ├── CET
    │       ├── CST6CDT
    │       ├── Cuba
    │       ├── EET
    │       ├── Egypt
    │       ├── Eire
    │       ├── EST
    │       ├── EST5EDT
    │       ├── GB
    │       ├── GB-Eire
    │       ├── GMT
    │       ├── GMT+0
    │       ├── GMT-0
    │       ├── GMT0
    │       ├── Greenwich
    │       ├── Hongkong
    │       ├── HST
    │       ├── Iceland
    │       ├── Iran
    │       ├── Israel
    │       ├── Jamaica
    │       ├── Japan
    │       ├── Kwajalein
    │       ├── Libya
    │       ├── MET
    │       ├── MST
    │       ├── MST7MDT
    │       ├── Navajo
    │       ├── NZ
    │       ├── NZ-CHAT
    │       ├── Poland
    │       ├── Portugal
    │       ├── PRC
    │       ├── PST8PDT
    │       ├── ROC
    │       ├── ROK
    │       ├── Singapore
    │       ├── Turkey
    │       ├── UCT
    │       ├── Universal
    │       ├── UTC
    │       ├── W-SU
    │       ├── WET
    │       ├── Zulu
    │       ├── Africa
    │       │   ├── Abidjan
    │       │   ├── Accra
    │       │   ├── Addis_Ababa
    │       │   ├── Algiers
    │       │   ├── Asmara
    │       │   ├── Asmera
    │       │   ├── Bamako
    │       │   ├── Bangui
    │       │   ├── Banjul
    │       │   ├── Bissau
    │       │   ├── Blantyre
    │       │   ├── Brazzaville
    │       │   ├── Bujumbura
    │       │   ├── Cairo
    │       │   ├── Casablanca
    │       │   ├── Ceuta
    │       │   ├── Conakry
    │       │   ├── Dakar
    │       │   ├── Dar_es_Salaam
    │       │   ├── Djibouti
    │       │   ├── Douala
    │       │   ├── El_Aaiun
    │       │   ├── Freetown
    │       │   ├── Gaborone
    │       │   ├── Harare
    │       │   ├── Johannesburg
    │       │   ├── Juba
    │       │   ├── Kampala
    │       │   ├── Khartoum
    │       │   ├── Kigali
    │       │   ├── Kinshasa
    │       │   ├── Lagos
    │       │   ├── Libreville
    │       │   ├── Lome
    │       │   ├── Luanda
    │       │   ├── Lubumbashi
    │       │   ├── Lusaka
    │       │   ├── Malabo
    │       │   ├── Maputo
    │       │   ├── Maseru
    │       │   ├── Mbabane
    │       │   ├── Mogadishu
    │       │   ├── Monrovia
    │       │   ├── Nairobi
    │       │   ├── Ndjamena
    │       │   ├── Niamey
    │       │   ├── Nouakchott
    │       │   ├── Ouagadougou
    │       │   ├── Porto-Novo
    │       │   ├── Sao_Tome
    │       │   ├── Timbuktu
    │       │   ├── Tripoli
    │       │   ├── Tunis
    │       │   └── Windhoek
    │       ├── America
    │       │   ├── Adak
    │       │   ├── Anchorage
    │       │   ├── Anguilla
    │       │   ├── Antigua
    │       │   ├── Araguaina
    │       │   ├── Aruba
    │       │   ├── Asuncion
    │       │   ├── Atikokan
    │       │   ├── Atka
    │       │   ├── Bahia
    │       │   ├── Bahia_Banderas
    │       │   ├── Barbados
    │       │   ├── Belem
    │       │   ├── Belize
    │       │   ├── Blanc-Sablon
    │       │   ├── Boa_Vista
    │       │   ├── Bogota
    │       │   ├── Boise
    │       │   ├── Buenos_Aires
    │       │   ├── Cambridge_Bay
    │       │   ├── Campo_Grande
    │       │   ├── Cancun
    │       │   ├── Caracas
    │       │   ├── Catamarca
    │       │   ├── Cayenne
    │       │   ├── Cayman
    │       │   ├── Chicago
    │       │   ├── Chihuahua
    │       │   ├── Coral_Harbour
    │       │   ├── Cordoba
    │       │   ├── Costa_Rica
    │       │   ├── Creston
    │       │   ├── Cuiaba
    │       │   ├── Curacao
    │       │   ├── Danmarkshavn
    │       │   ├── Dawson
    │       │   ├── Dawson_Creek
    │       │   ├── Denver
    │       │   ├── Detroit
    │       │   ├── Dominica
    │       │   ├── Edmonton
    │       │   ├── Eirunepe
    │       │   ├── El_Salvador
    │       │   ├── Ensenada
    │       │   ├── Fort_Nelson
    │       │   ├── Fort_Wayne
    │       │   ├── Fortaleza
    │       │   ├── Glace_Bay
    │       │   ├── Godthab
    │       │   ├── Goose_Bay
    │       │   ├── Grand_Turk
    │       │   ├── Grenada
    │       │   ├── Guadeloupe
    │       │   ├── Guatemala
    │       │   ├── Guayaquil
    │       │   ├── Guyana
    │       │   ├── Halifax
    │       │   ├── Havana
    │       │   ├── Hermosillo
    │       │   ├── Indianapolis
    │       │   ├── Inuvik
    │       │   ├── Iqaluit
    │       │   ├── Jamaica
    │       │   ├── Jujuy
    │       │   ├── Juneau
    │       │   ├── Knox_IN
    │       │   ├── Kralendijk
    │       │   ├── La_Paz
    │       │   ├── Lima
    │       │   ├── Los_Angeles
    │       │   ├── Louisville
    │       │   ├── Lower_Princes
    │       │   ├── Maceio
    │       │   ├── Managua
    │       │   ├── Manaus
    │       │   ├── Marigot
    │       │   ├── Martinique
    │       │   ├── Matamoros
    │       │   ├── Mazatlan
    │       │   ├── Mendoza
    │       │   ├── Menominee
    │       │   ├── Merida
    │       │   ├── Metlakatla
    │       │   ├── Mexico_City
    │       │   ├── Miquelon
    │       │   ├── Moncton
    │       │   ├── Monterrey
    │       │   ├── Montevideo
    │       │   ├── Montreal
    │       │   ├── Montserrat
    │       │   ├── Nassau
    │       │   ├── New_York
    │       │   ├── Nipigon
    │       │   ├── Nome
    │       │   ├── Noronha
    │       │   ├── Nuuk
    │       │   ├── Ojinaga
    │       │   ├── Panama
    │       │   ├── Pangnirtung
    │       │   ├── Paramaribo
    │       │   ├── Phoenix
    │       │   ├── Port-au-Prince
    │       │   ├── Port_of_Spain
    │       │   ├── Porto_Acre
    │       │   ├── Porto_Velho
    │       │   ├── Puerto_Rico
    │       │   ├── Punta_Arenas
    │       │   ├── Rainy_River
    │       │   ├── Rankin_Inlet
    │       │   ├── Recife
    │       │   ├── Regina
    │       │   ├── Resolute
    │       │   ├── Rio_Branco
    │       │   ├── Rosario
    │       │   ├── Santa_Isabel
    │       │   ├── Santarem
    │       │   ├── Santiago
    │       │   ├── Santo_Domingo
    │       │   ├── Sao_Paulo
    │       │   ├── Scoresbysund
    │       │   ├── Shiprock
    │       │   ├── Sitka
    │       │   ├── St_Barthelemy
    │       │   ├── St_Johns
    │       │   ├── St_Kitts
    │       │   ├── St_Lucia
    │       │   ├── St_Thomas
    │       │   ├── St_Vincent
    │       │   ├── Swift_Current
    │       │   ├── Tegucigalpa
    │       │   ├── Thule
    │       │   ├── Thunder_Bay
    │       │   ├── Tijuana
    │       │   ├── Toronto
    │       │   ├── Tortola
    │       │   ├── Vancouver
    │       │   ├── Virgin
    │       │   ├── Whitehorse
    │       │   ├── Winnipeg
    │       │   ├── Yakutat
    │       │   ├── Yellowknife
    │       │   ├── Argentina
    │       │   │   ├── Buenos_Aires
    │       │   │   ├── Catamarca
    │       │   │   ├── ComodRivadavia
    │       │   │   ├── Cordoba
    │       │   │   ├── Jujuy
    │       │   │   ├── La_Rioja
    │       │   │   ├── Mendoza
    │       │   │   ├── Rio_Gallegos
    │       │   │   ├── Salta
    │       │   │   ├── San_Juan
    │       │   │   ├── San_Luis
    │       │   │   ├── Tucuman
    │       │   │   └── Ushuaia
    │       │   ├── Indiana
    │       │   │   ├── Indianapolis
    │       │   │   ├── Knox
    │       │   │   ├── Marengo
    │       │   │   ├── Petersburg
    │       │   │   ├── Tell_City
    │       │   │   ├── Vevay
    │       │   │   ├── Vincennes
    │       │   │   └── Winamac
    │       │   ├── Kentucky
    │       │   │   ├── Louisville
    │       │   │   └── Monticello
    │       │   └── North_Dakota
    │       │       ├── Beulah
    │       │       ├── Center
    │       │       └── New_Salem
    │       ├── Antarctica
    │       │   ├── Casey
    │       │   ├── Davis
    │       │   ├── DumontDUrville
    │       │   ├── Macquarie
    │       │   ├── Mawson
    │       │   ├── McMurdo
    │       │   ├── Palmer
    │       │   ├── Rothera
    │       │   ├── South_Pole
    │       │   ├── Syowa
    │       │   ├── Troll
    │       │   └── Vostok
    │       ├── Arctic
    │       │   └── Longyearbyen
    │       ├── Asia
    │       │   ├── Aden
    │       │   ├── Almaty
    │       │   ├── Amman
    │       │   ├── Anadyr
    │       │   ├── Aqtau
    │       │   ├── Aqtobe
    │       │   ├── Ashgabat
    │       │   ├── Ashkhabad
    │       │   ├── Atyrau
    │       │   ├── Baghdad
    │       │   ├── Bahrain
    │       │   ├── Baku
    │       │   ├── Bangkok
    │       │   ├── Barnaul
    │       │   ├── Beirut
    │       │   ├── Bishkek
    │       │   ├── Brunei
    │       │   ├── Calcutta
    │       │   ├── Chita
    │       │   ├── Choibalsan
    │       │   ├── Chongqing
    │       │   ├── Chungking
    │       │   ├── Colombo
    │       │   ├── Dacca
    │       │   ├── Damascus
    │       │   ├── Dhaka
    │       │   ├── Dili
    │       │   ├── Dubai
    │       │   ├── Dushanbe
    │       │   ├── Famagusta
    │       │   ├── Gaza
    │       │   ├── Harbin
    │       │   ├── Hebron
    │       │   ├── Ho_Chi_Minh
    │       │   ├── Hong_Kong
    │       │   ├── Hovd
    │       │   ├── Irkutsk
    │       │   ├── Istanbul
    │       │   ├── Jakarta
    │       │   ├── Jayapura
    │       │   ├── Jerusalem
    │       │   ├── Kabul
    │       │   ├── Kamchatka
    │       │   ├── Karachi
    │       │   ├── Kashgar
    │       │   ├── Kathmandu
    │       │   ├── Katmandu
    │       │   ├── Khandyga
    │       │   ├── Kolkata
    │       │   ├── Krasnoyarsk
    │       │   ├── Kuala_Lumpur
    │       │   ├── Kuching
    │       │   ├── Kuwait
    │       │   ├── Macao
    │       │   ├── Macau
    │       │   ├── Magadan
    │       │   ├── Makassar
    │       │   ├── Manila
    │       │   ├── Muscat
    │       │   ├── Nicosia
    │       │   ├── Novokuznetsk
    │       │   ├── Novosibirsk
    │       │   ├── Omsk
    │       │   ├── Oral
    │       │   ├── Phnom_Penh
    │       │   ├── Pontianak
    │       │   ├── Pyongyang
    │       │   ├── Qatar
    │       │   ├── Qostanay
    │       │   ├── Qyzylorda
    │       │   ├── Rangoon
    │       │   ├── Riyadh
    │       │   ├── Saigon
    │       │   ├── Sakhalin
    │       │   ├── Samarkand
    │       │   ├── Seoul
    │       │   ├── Shanghai
    │       │   ├── Singapore
    │       │   ├── Srednekolymsk
    │       │   ├── Taipei
    │       │   ├── Tashkent
    │       │   ├── Tbilisi
    │       │   ├── Tehran
    │       │   ├── Tel_Aviv
    │       │   ├── Thimbu
    │       │   ├── Thimphu
    │       │   ├── Tokyo
    │       │   ├── Tomsk
    │       │   ├── Ujung_Pandang
    │       │   ├── Ulaanbaatar
    │       │   ├── Ulan_Bator
    │       │   ├── Urumqi
    │       │   ├── Ust-Nera
    │       │   ├── Vientiane
    │       │   ├── Vladivostok
    │       │   ├── Yakutsk
    │       │   ├── Yangon
    │       │   ├── Yekaterinburg
    │       │   └── Yerevan
    │       ├── Atlantic
    │       │   ├── Azores
    │       │   ├── Bermuda
    │       │   ├── Canary
    │       │   ├── Cape_Verde
    │       │   ├── Faeroe
    │       │   ├── Faroe
    │       │   ├── Jan_Mayen
    │       │   ├── Madeira
    │       │   ├── Reykjavik
    │       │   ├── South_Georgia
    │       │   ├── St_Helena
    │       │   └── Stanley
    │       ├── Australia
    │       │   ├── ACT
    │       │   ├── Adelaide
    │       │   ├── Brisbane
    │       │   ├── Broken_Hill
    │       │   ├── Canberra
    │       │   ├── Currie
    │       │   ├── Darwin
    │       │   ├── Eucla
    │       │   ├── Hobart
    │       │   ├── LHI
    │       │   ├── Lindeman
    │       │   ├── Lord_Howe
    │       │   ├── Melbourne
    │       │   ├── North
    │       │   ├── NSW
    │       │   ├── Perth
    │       │   ├── Queensland
    │       │   ├── South
    │       │   ├── Sydney
    │       │   ├── Tasmania
    │       │   ├── Victoria
    │       │   ├── West
    │       │   └── Yancowinna
    │       ├── Brazil
    │       │   ├── Acre
    │       │   ├── DeNoronha
    │       │   ├── East
    │       │   └── West
    │       ├── Canada
    │       │   ├── Atlantic
    │       │   ├── Central
    │       │   ├── Eastern
    │       │   ├── Mountain
    │       │   ├── Newfoundland
    │       │   ├── Pacific
    │       │   ├── Saskatchewan
    │       │   └── Yukon
    │       ├── Chile
    │       │   ├── Continental
    │       │   └── EasterIsland
    │       ├── Etc
    │       │   ├── GMT
    │       │   ├── GMT+0
    │       │   ├── GMT+1
    │       │   ├── GMT+10
    │       │   ├── GMT+11
    │       │   ├── GMT+12
    │       │   ├── GMT+2
    │       │   ├── GMT+3
    │       │   ├── GMT+4
    │       │   ├── GMT+5
    │       │   ├── GMT+6
    │       │   ├── GMT+7
    │       │   ├── GMT+8
    │       │   ├── GMT+9
    │       │   ├── GMT-0
    │       │   ├── GMT-1
    │       │   ├── GMT-10
    │       │   ├── GMT-11
    │       │   ├── GMT-12
    │       │   ├── GMT-13
    │       │   ├── GMT-14
    │       │   ├── GMT-2
    │       │   ├── GMT-3
    │       │   ├── GMT-4
    │       │   ├── GMT-5
    │       │   ├── GMT-6
    │       │   ├── GMT-7
    │       │   ├── GMT-8
    │       │   ├── GMT-9
    │       │   ├── GMT0
    │       │   ├── Greenwich
    │       │   ├── UCT
    │       │   ├── Universal
    │       │   ├── UTC
    │       │   └── Zulu
    │       ├── Europe
    │       │   ├── Amsterdam
    │       │   ├── Andorra
    │       │   ├── Astrakhan
    │       │   ├── Athens
    │       │   ├── Belfast
    │       │   ├── Belgrade
    │       │   ├── Berlin
    │       │   ├── Bratislava
    │       │   ├── Brussels
    │       │   ├── Bucharest
    │       │   ├── Budapest
    │       │   ├── Busingen
    │       │   ├── Chisinau
    │       │   ├── Copenhagen
    │       │   ├── Dublin
    │       │   ├── Gibraltar
    │       │   ├── Guernsey
    │       │   ├── Helsinki
    │       │   ├── Isle_of_Man
    │       │   ├── Istanbul
    │       │   ├── Jersey
    │       │   ├── Kaliningrad
    │       │   ├── Kiev
    │       │   ├── Kirov
    │       │   ├── Kyiv
    │       │   ├── Lisbon
    │       │   ├── Ljubljana
    │       │   ├── London
    │       │   ├── Luxembourg
    │       │   ├── Madrid
    │       │   ├── Malta
    │       │   ├── Mariehamn
    │       │   ├── Minsk
    │       │   ├── Monaco
    │       │   ├── Moscow
    │       │   ├── Nicosia
    │       │   ├── Oslo
    │       │   ├── Paris
    │       │   ├── Podgorica
    │       │   ├── Prague
    │       │   ├── Riga
    │       │   ├── Rome
    │       │   ├── Samara
    │       │   ├── San_Marino
    │       │   ├── Sarajevo
    │       │   ├── Saratov
    │       │   ├── Simferopol
    │       │   ├── Skopje
    │       │   ├── Sofia
    │       │   ├── Stockholm
    │       │   ├── Tallinn
    │       │   ├── Tirane
    │       │   ├── Tiraspol
    │       │   ├── Ulyanovsk
    │       │   ├── Uzhgorod
    │       │   ├── Vaduz
    │       │   ├── Vatican
    │       │   ├── Vienna
    │       │   ├── Vilnius
    │       │   ├── Volgograd
    │       │   ├── Warsaw
    │       │   ├── Zagreb
    │       │   ├── Zaporozhye
    │       │   └── Zurich
    │       ├── Indian
    │       │   ├── Antananarivo
    │       │   ├── Chagos
    │       │   ├── Christmas
    │       │   ├── Cocos
    │       │   ├── Comoro
    │       │   ├── Kerguelen
    │       │   ├── Mahe
    │       │   ├── Maldives
    │       │   ├── Mauritius
    │       │   ├── Mayotte
    │       │   └── Reunion
    │       ├── Mexico
    │       │   ├── BajaNorte
    │       │   ├── BajaSur
    │       │   └── General
    │       ├── Pacific
    │       │   ├── Apia
    │       │   ├── Auckland
    │       │   ├── Bougainville
    │       │   ├── Chatham
    │       │   ├── Chuuk
    │       │   ├── Easter
    │       │   ├── Efate
    │       │   ├── Enderbury
    │       │   ├── Fakaofo
    │       │   ├── Fiji
    │       │   ├── Funafuti
    │       │   ├── Galapagos
    │       │   ├── Gambier
    │       │   ├── Guadalcanal
    │       │   ├── Guam
    │       │   ├── Honolulu
    │       │   ├── Johnston
    │       │   ├── Kanton
    │       │   ├── Kiritimati
    │       │   ├── Kosrae
    │       │   ├── Kwajalein
    │       │   ├── Majuro
    │       │   ├── Marquesas
    │       │   ├── Midway
    │       │   ├── Nauru
    │       │   ├── Niue
    │       │   ├── Norfolk
    │       │   ├── Noumea
    │       │   ├── Pago_Pago
    │       │   ├── Palau
    │       │   ├── Pitcairn
    │       │   ├── Pohnpei
    │       │   ├── Ponape
    │       │   ├── Port_Moresby
    │       │   ├── Rarotonga
    │       │   ├── Saipan
    │       │   ├── Samoa
    │       │   ├── Tahiti
    │       │   ├── Tarawa
    │       │   ├── Tongatapu
    │       │   ├── Truk
    │       │   ├── Wake
    │       │   ├── Wallis
    │       │   └── Yap
    │       ├── SystemV
    │       │   ├── AST4
    │       │   ├── AST4ADT
    │       │   ├── CST6
    │       │   ├── CST6CDT
    │       │   ├── EST5
    │       │   ├── EST5EDT
    │       │   ├── HST10
    │       │   ├── MST7
    │       │   ├── MST7MDT
    │       │   ├── PST8
    │       │   ├── PST8PDT
    │       │   ├── YST9
    │       │   └── YST9YDT
    │       └── US
    │           ├── Alaska
    │           ├── Aleutian
    │           ├── Arizona
    │           ├── Central
    │           ├── East-Indiana
    │           ├── Eastern
    │           ├── Hawaii
    │           ├── Indiana-Starke
    │           ├── Michigan
    │           ├── Mountain
    │           ├── Pacific
    │           └── Samoa
    ├── _tk_data
    │   ├── bgerror.tcl
    │   ├── button.tcl
    │   ├── choosedir.tcl
    │   ├── clrpick.tcl
    │   ├── comdlg.tcl
    │   ├── console.tcl
    │   ├── dialog.tcl
    │   ├── entry.tcl
    │   ├── focus.tcl
    │   ├── fontchooser.tcl
    │   ├── iconlist.tcl
    │   ├── icons.tcl
    │   ├── license.terms
    │   ├── listbox.tcl
    │   ├── megawidget.tcl
    │   ├── menu.tcl
    │   ├── mkpsenc.tcl
    │   ├── msgbox.tcl
    │   ├── obsolete.tcl
    │   ├── optMenu.tcl
    │   ├── palette.tcl
    │   ├── panedwindow.tcl
    │   ├── pkgIndex.tcl
    │   ├── safetk.tcl
    │   ├── scale.tcl
    │   ├── scrlbar.tcl
    │   ├── spinbox.tcl
    │   ├── tclIndex
    │   ├── tearoff.tcl
    │   ├── text.tcl
    │   ├── tk.tcl
    │   ├── tkfbox.tcl
    │   ├── unsupported.tcl
    │   ├── xmfbox.tcl
    │   ├── images
    │   │   ├── logo.eps
    │   │   ├── logo100.gif
    │   │   ├── logo64.gif
    │   │   ├── logoLarge.gif
    │   │   ├── logoMed.gif
    │   │   ├── pwrdLogo.eps
    │   │   ├── pwrdLogo100.gif
    │   │   ├── pwrdLogo150.gif
    │   │   ├── pwrdLogo175.gif
    │   │   ├── pwrdLogo200.gif
    │   │   ├── pwrdLogo75.gif
    │   │   ├── README
    │   │   └── tai-ku.gif
    │   ├── msgs
    │   │   ├── cs.msg
    │   │   ├── da.msg
    │   │   ├── de.msg
    │   │   ├── el.msg
    │   │   ├── en.msg
    │   │   ├── en_gb.msg
    │   │   ├── eo.msg
    │   │   ├── es.msg
    │   │   ├── fi.msg
    │   │   ├── fr.msg
    │   │   ├── hu.msg
    │   │   ├── it.msg
    │   │   ├── nl.msg
    │   │   ├── pl.msg
    │   │   ├── pt.msg
    │   │   ├── ru.msg
    │   │   ├── sv.msg
    │   │   └── zh_cn.msg
    │   └── ttk
    │       ├── altTheme.tcl
    │       ├── aquaTheme.tcl
    │       ├── button.tcl
    │       ├── clamTheme.tcl
    │       ├── classicTheme.tcl
    │       ├── combobox.tcl
    │       ├── cursors.tcl
    │       ├── defaults.tcl
    │       ├── entry.tcl
    │       ├── fonts.tcl
    │       ├── menubutton.tcl
    │       ├── notebook.tcl
    │       ├── panedwindow.tcl
    │       ├── progress.tcl
    │       ├── scale.tcl
    │       ├── scrollbar.tcl
    │       ├── sizegrip.tcl
    │       ├── spinbox.tcl
    │       ├── treeview.tcl
    │       ├── ttk.tcl
    │       ├── utils.tcl
    │       ├── vistaTheme.tcl
    │       ├── winTheme.tcl
    │       └── xpTheme.tcl
    ├── numpy
    │   ├── core
    │   │   ├── _multiarray_tests.cp312-win_amd64.pyd
    │   │   └── _multiarray_umath.cp312-win_amd64.pyd
    │   ├── fft
    │   │   └── _pocketfft_internal.cp312-win_amd64.pyd
    │   ├── linalg
    │   │   └── _umath_linalg.cp312-win_amd64.pyd
    │   └── random
    │       ├── _bounded_integers.cp312-win_amd64.pyd
    │       ├── _common.cp312-win_amd64.pyd
    │       ├── _generator.cp312-win_amd64.pyd
    │       ├── _mt19937.cp312-win_amd64.pyd
    │       ├── _pcg64.cp312-win_amd64.pyd
    │       ├── _philox.cp312-win_amd64.pyd
    │       ├── _sfc64.cp312-win_amd64.pyd
    │       ├── bit_generator.cp312-win_amd64.pyd
    │       └── mtrand.cp312-win_amd64.pyd
    ├── numpy.libs
    │   └── libopenblas64__v0.3.23-293-gc2f4bdbb-gcc_10_3_0-2bde3a66a51006b2b53eb373ff767a3f.dll
    ├── OpenGL
    │   └── DLLS
    │       ├── freeglut32.vc10.dll
    │       ├── freeglut32.vc14.dll
    │       ├── freeglut32.vc9.dll
    │       ├── freeglut64.vc10.dll
    │       ├── freeglut64.vc14.dll
    │       ├── freeglut64.vc9.dll
    │       ├── freeglut_COPYING.txt
    │       ├── freeglut_README.txt
    │       ├── gle32.vc10.dll
    │       ├── gle32.vc14.dll
    │       ├── gle32.vc9.dll
    │       ├── gle64.vc10.dll
    │       ├── gle64.vc14.dll
    │       ├── gle64.vc9.dll
    │       ├── gle_AUTHORS
    │       ├── gle_COPYING
    │       ├── gle_COPYING.src
    │       └── GLE_WIN32_README.txt
    ├── OpenGL_accelerate
    │   ├── arraydatatype.cp312-win_amd64.pyd
    │   ├── buffers_formathandler.cp312-win_amd64.pyd
    │   ├── errorchecker.cp312-win_amd64.pyd
    │   ├── formathandler.cp312-win_amd64.pyd
    │   ├── latebind.cp312-win_amd64.pyd
    │   ├── nones_formathandler.cp312-win_amd64.pyd
    │   ├── numpy_formathandler.cp312-win_amd64.pyd
    │   ├── vbo.cp312-win_amd64.pyd
    │   └── wrapper.cp312-win_amd64.pyd
    ├── psutil
    │   └── _psutil_windows.pyd
    ├── pygame
    │   ├── _freetype.cp312-win_amd64.pyd
    │   ├── base.cp312-win_amd64.pyd
    │   ├── bufferproxy.cp312-win_amd64.pyd
    │   ├── color.cp312-win_amd64.pyd
    │   ├── constants.cp312-win_amd64.pyd
    │   ├── display.cp312-win_amd64.pyd
    │   ├── draw.cp312-win_amd64.pyd
    │   ├── event.cp312-win_amd64.pyd
    │   ├── font.cp312-win_amd64.pyd
    │   ├── freesansbold.ttf
    │   ├── freetype.dll
    │   ├── image.cp312-win_amd64.pyd
    │   ├── imageext.cp312-win_amd64.pyd
    │   ├── joystick.cp312-win_amd64.pyd
    │   ├── key.cp312-win_amd64.pyd
    │   ├── libjpeg-9.dll
    │   ├── libogg-0.dll
    │   ├── libopus-0.dll
    │   ├── libpng16-16.dll
    │   ├── mask.cp312-win_amd64.pyd
    │   ├── math.cp312-win_amd64.pyd
    │   ├── mixer.cp312-win_amd64.pyd
    │   ├── mixer_music.cp312-win_amd64.pyd
    │   ├── mouse.cp312-win_amd64.pyd
    │   ├── pixelarray.cp312-win_amd64.pyd
    │   ├── pixelcopy.cp312-win_amd64.pyd
    │   ├── pygame_icon.bmp
    │   ├── rect.cp312-win_amd64.pyd
    │   ├── rwobject.cp312-win_amd64.pyd
    │   ├── scrap.cp312-win_amd64.pyd
    │   ├── SDL2.dll
    │   ├── SDL2_image.dll
    │   ├── SDL2_mixer.dll
    │   ├── SDL2_ttf.dll
    │   ├── surface.cp312-win_amd64.pyd
    │   ├── surflock.cp312-win_amd64.pyd
    │   ├── time.cp312-win_amd64.pyd
    │   ├── transform.cp312-win_amd64.pyd
    │   ├── zlib1.dll
    │   └── _sdl2
    │       ├── audio.cp312-win_amd64.pyd
    │       ├── sdl2.cp312-win_amd64.pyd
    │       └── video.cp312-win_amd64.pyd
    ├── pywin32_system32
    │   └── pywintypes312.dll
    ├── setuptools
    │   └── _vendor
    │       ├── importlib_metadata-8.0.0.dist-info
    │       │   ├── INSTALLER
    │       │   ├── LICENSE
    │       │   ├── METADATA
    │       │   ├── RECORD
    │       │   ├── REQUESTED
    │       │   ├── top_level.txt
    │       │   └── WHEEL
    │       └── jaraco
    │           └── text
    │               └── Lorem ipsum.txt
    ├── src
    │   ├── background.png
    │   ├── icon.ico
    │   ├── icon.png
    │   ├── fonts
    │   │   ├── DS-DIGIB.TTF
    │   │   ├── FranklinGothicHeavyRegular.ttf
    │   │   └── LetterGothicStd-Bold.ttf
    │   └── img
    │       ├── background.png
    │       ├── blue_cable_off.png
    │       ├── blue_cable_on.png
    │       ├── hourglass.png
    │       ├── human_skill+boost.png
    │       ├── red_cable_off.png
    │       ├── red_cable_on.png
    │       ├── shop.png
    │       ├── shop_bord.png
    │       ├── shop_fond.png
    │       ├── temporal_matrix.png
    │       ├── timeline.png
    │       ├── timeUnits.png
    │       ├── TPS.png
    │       ├── upgrade.png
    │       ├── upgrade_bord.png
    │       ├── upgrade_fond.png
    │       ├── upgrade_original.png
    │       ├── usb_boost.png
    │       ├── usb_boost_2.png
    │       ├── usb_boost_5.png
    │       ├── buildings
    │       │   ├── ai.png
    │       │   ├── antimatter_central.png
    │       │   ├── aqueduct.png
    │       │   ├── base_1.png
    │       │   ├── base_2.png
    │       │   ├── base_3.png
    │       │   ├── base_4.png
    │       │   ├── base_5.png
    │       │   ├── base_6.png
    │       │   ├── campfire.png
    │       │   ├── car.png
    │       │   ├── cash.png
    │       │   ├── castle.png
    │       │   ├── church.png
    │       │   ├── electronic.png
    │       │   ├── factory.png
    │       │   ├── farming.png
    │       │   ├── hunting.png
    │       │   ├── internet.png
    │       │   ├── nuclear_central.png
    │       │   ├── painting.png
    │       │   ├── printing.png
    │       │   ├── pyramid.png
    │       │   ├── rail.png
    │       │   ├── rocket.png
    │       │   ├── school.png
    │       │   ├── spaceship.png
    │       │   ├── steam_engine.png
    │       │   ├── temple.png
    │       │   └── time_machine.png
    │       └── upgrades
    │           ├── artefact.png
    │           ├── base_timeline.png
    │           ├── black_hole.png
    │           ├── brush.png
    │           ├── coal.png
    │           ├── development.png
    │           ├── drivers.png
    │           ├── engineers.png
    │           ├── flint.png
    │           ├── fuel.png
    │           ├── gold.png
    │           ├── hoe.png
    │           ├── locomotive.png
    │           ├── maths.png
    │           ├── monk.png
    │           ├── niv0.png
    │           ├── niv1.png
    │           ├── niv2.png
    │           ├── niv3.png
    │           ├── niv4.png
    │           ├── niv5.png
    │           ├── niv6.png
    │           ├── paper.png
    │           ├── printed_circuit.png
    │           ├── reactor.png
    │           ├── servers.png
    │           ├── soldier.png
    │           ├── stone.png
    │           ├── students.png
    │           ├── time.png
    │           ├── timeline_unlock_image.png
    │           ├── uranium.png
    │           └── weapons.png
    ├── tcl8
    │   ├── 8.4
    │   │   ├── platform-1.0.19.tm
    │   │   └── platform
    │   │       └── shell-1.1.4.tm
    │   ├── 8.5
    │   │   ├── msgcat-1.6.1.tm
    │   │   └── tcltest-2.5.5.tm
    │   └── 8.6
    │       └── http-2.9.8.tm
    ├── wheel-0.44.0.dist-info
    │   ├── entry_points.txt
    │   ├── INSTALLER
    │   ├── LICENSE.txt
    │   ├── METADATA
    │   ├── RECORD
    │   └── WHEEL
    ├── win32
    │   └── win32pdh.pyd
    └── yaml
        └── _yaml.cp312-win_amd64.pyd





'''