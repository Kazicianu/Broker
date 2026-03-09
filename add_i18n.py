import re

def main():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Dictionary of exact string matches to add data-i18n attributes to existing tags
    replacements = [
        (r'>Despre mine<', r' data-i18n="nav_about">Despre mine<'),
        (r'>Servicii<', r' data-i18n="nav_services">Servicii<'),
        (r'>Asigurări<', r' data-i18n="nav_insurance">Asigurări<'),
        (r'>Creditare<', r' data-i18n="nav_credit">Creditare<'),
        (r'>Păreri<', r' data-i18n="nav_testimonials">Păreri<'),
        (r'>FAQ<', r' data-i18n="nav_faq">FAQ<'),
        (r'>Contactează-mă<', r' data-i18n="nav_contact">Contactează-mă<'),

        (r'Disponibil pentru consultanță', r'<span data-i18n="hero_badge">Disponibil pentru consultanță</span>'),
        (r'Salut, sunt<br>', r'<span data-i18n="hero_title_1">Salut, sunt<br></span>'),
        (r'<p class="hero-subtitle">Consultant în Asigurări, Creditare & Imobiliar</p>', r'<p class="hero-subtitle" data-i18n="hero_subtitle">Consultant în Asigurări, Creditare & Imobiliar</p>'),
        (r'<p class="hero-description">\s*Te ajut să găsești.*?\s*</p>', r'<p class="hero-description" data-i18n="hero_desc">\n          Te ajut să găsești soluțiile financiare potrivite nevoilor tale. De la asigurări complete la credite\n          avantajoase, sunt alături de tine la fiecare pas.\n        </p>'),
        (r'📞 Sună-mă acum', r'<span data-i18n="hero_call">📞 Sună-mă acum</span>'),
        (r'💬 WhatsApp', r'<span data-i18n="hero_wa">💬 WhatsApp</span>'),
        (r'Descoperă serviciile →', r'<span data-i18n="hero_services">Descoperă serviciile →</span>'),

        (r'<p class="profile-title">Consultant & Broker Financiar</p>', r'<p class="profile-title" data-i18n="prof_title">Consultant & Broker Financiar</p>'),
        (r'<div class="stat-label">Domenii</div>', r'<div class="stat-label" data-i18n="prof_stat1">Domenii</div>'),
        (r'<div class="stat-label">Tipuri asigurări</div>', r'<div class="stat-label" data-i18n="prof_stat2">Tipuri asigurări</div>'),
        (r'<div class="stat-label">Dedicare</div>', r'<div class="stat-label" data-i18n="prof_stat3">Dedicare</div>'),
        (r'Solicită o consultanță gratuită\s*</a>', r'<span data-i18n="prof_btn">Solicită o consultanță gratuită</span>\n          </a>'),

        (r'<span class="section-label">Despre mine</span>', r'<span class="section-label" data-i18n="about_label">Despre mine</span>'),
        (r'<h2 class="section-title">Partenerul tău financiar de încredere</h2>', r'<h2 class="section-title" data-i18n="about_title">Partenerul tău financiar de încredere</h2>'),
        (r'<p>\s*Sunt Dragoș Vîrjoghe.*?\s*</p>', r'<p data-i18n="about_p1">\n            Sunt Dragoș Vîrjoghe, și mă ocup cu pasiune de a oferi soluții personalizate în domeniul imobiliar,\n            asigurărilor și creditării. Am ales să îmi extind activitatea pentru a putea acoperi toate nevoile tale\n            financiare dintr-un singur loc.\n          </p>'),
        (r'<p>\s*Fie că ai nevoie de o asigurare RCA.*?\s*</p>', r'<p data-i18n="about_p2">\n            Fie că ai nevoie de o asigurare RCA, un credit ipotecar sau consiliere în domeniul imobiliar, sunt aici să\n            te ghidez prin fiecare etapă a procesului — simplu, transparent și fără costuri ascunse.\n          </p>'),
        (r'<h4>Consultanță personalizată</h4>', r'<h4 data-i18n="about_h1_t">Consultanță personalizată</h4>'),
        (r'<p>Fiecare client primește atenție individuală și soluții adaptate nevoilor sale specifice.</p>', r'<p data-i18n="about_h1_d">Fiecare client primește atenție individuală și soluții adaptate nevoilor sale specifice.</p>'),
        (r'<h4>Rapiditate și eficiență</h4>', r'<h4 data-i18n="about_h2_t">Rapiditate și eficiență</h4>'),
        (r'<p>Procesare rapidă, fără birocrație inutilă. Timpul tău contează.</p>', r'<p data-i18n="about_h2_d">Procesare rapidă, fără birocrație inutilă. Timpul tău contează.</p>'),
        (r'<h4>Transparență totală</h4>', r'<h4 data-i18n="about_h3_t">Transparență totală</h4>'),
        (r'<p>Informații clare, fără costuri ascunse. Decizii informate, rezultate pe măsură.</p>', r'<p data-i18n="about_h3_d">Informații clare, fără costuri ascunse. Decizii informate, rezultate pe măsură.</p>'),

        (r'<span class="section-label">Ce ofer</span>', r'<span class="section-label" data-i18n="srv_label">Ce ofer</span>'),
        (r'<h2 class="section-title">Serviciile mele</h2>', r'<h2 class="section-title" data-i18n="srv_title">Serviciile mele</h2>'),
        (r'<p class="section-subtitle">\s*Trei domenii.*?\s*</p>', r'<p class="section-subtitle" data-i18n="srv_sub">\n          Trei domenii, un singur consultant. Toate soluțiile financiare de care ai nevoie, într-un singur loc.\n        </p>'),

        (r'<h3>Imobiliar</h3>', r'<h3 data-i18n="srv_imob_t">Imobiliar</h3>'),
        (r'<p>Consiliere completă în tranzacțiile imobiliare, de la identificarea proprietății ideale la finalizarea\s*actelor.</p>', r'<p data-i18n="srv_imob_p">Consiliere completă în tranzacțiile imobiliare, de la identificarea proprietății ideale la finalizarea\n              actelor.</p>'),
        (r'<li>Vânzare & cumpărare proprietăți</li>', r'<li data-i18n="srv_imob_l1">Vânzare & cumpărare proprietăți</li>'),
        (r'<li>Evaluare și consultanță</li>', r'<li data-i18n="srv_imob_l2">Evaluare și consultanță</li>'),
        (r'<li>Intermediere tranzacții</li>', r'<li data-i18n="srv_imob_l3">Intermediere tranzacții</li>'),
        (r'<li>Suport documentație</li>', r'<li data-i18n="srv_imob_l4">Suport documentație</li>'),

        (r'<h3>Asigurări</h3>', r'<h3 data-i18n="srv_asig_t">Asigurări</h3>'),
        (r'<p>Gama completă de asigurări pentru tine, familia ta și bunurile tale. Protecție maximă, prețuri\s*competitive.</p>', r'<p data-i18n="srv_asig_p">Gama completă de asigurări pentru tine, familia ta și bunurile tale. Protecție maximă, prețuri\n              competitive.</p>'),
        (r'<li>RCA & CASCO auto</li>', r'<li data-i18n="srv_asig_l1">RCA & CASCO auto</li>'),
        (r'<li>Asigurări locuință & bunuri</li>', r'<li data-i18n="srv_asig_l2">Asigurări locuință & bunuri</li>'),
        (r'<li>Asigurări de călătorie</li>', r'<li data-i18n="srv_asig_l3">Asigurări de călătorie</li>'),
        (r'<li>Asigurări de sănătate & viață</li>', r'<li data-i18n="srv_asig_l4">Asigurări de sănătate & viață</li>'),

        (r'<h3>Creditare</h3>', r'<h3 data-i18n="srv_cred_t">Creditare</h3>'),
        (r'<p>Soluții de creditare avantajoase, cu cele mai bune dobânzi de pe piață. Te ajut să alegi creditul\s*potrivit.</p>', r'<p data-i18n="srv_cred_p">Soluții de creditare avantajoase, cu cele mai bune dobânzi de pe piață. Te ajut să alegi creditul\n              potrivit.</p>'),
        (r'<li>Credite ipotecare</li>', r'<li data-i18n="srv_cred_l1">Credite ipotecare</li>'),
        (r'<li>Refinanțări avantajoase</li>', r'<li data-i18n="srv_cred_l2">Refinanțări avantajoase</li>'),
        (r'<li>Credite de nevoi personale</li>', r'<li data-i18n="srv_cred_l3">Credite de nevoi personale</li>'),
        (r'<li>Consultanță financiară</li>', r'<li data-i18n="srv_cred_l4">Consultanță financiară</li>'),

        (r'<span class="section-label">Asigurări</span>', r'<span class="section-label" data-i18n="ins_label">Asigurări</span>'),
        (r'<h2 class="section-title">Tipuri de asigurări disponibile</h2>', r'<h2 class="section-title" data-i18n="ins_title">Tipuri de asigurări disponibile</h2>'),
        (r'<p class="section-subtitle">\s*Protecție completă.*?\s*</p>', r'<p class="section-subtitle" data-i18n="ins_sub">\n          Protecție completă pentru fiecare aspect al vieții tale. Alege asigurarea potrivită.\n        </p>'),

        (r'<h4>RCA</h4>', r'<h4 data-i18n="ins_rca_t">RCA</h4>'),
        (r'<p>Asigurare obligatorie auto, prețuri competitive de la toate companiile.</p>', r'<p data-i18n="ins_rca_p">Asigurare obligatorie auto, prețuri competitive de la toate companiile.</p>'),
        (r'<h4>CASCO</h4>', r'<h4 data-i18n="ins_casco_t">CASCO</h4>'),
        (r'<p>Protecție completă pentru autovehiculul tău, inclusiv furt și daune proprii.</p>', r'<p data-i18n="ins_casco_p">Protecție completă pentru autovehiculul tău, inclusiv furt și daune proprii.</p>'),
        (r'<h4>Locuință</h4>', r'<h4 data-i18n="ins_loc_t">Locuință</h4>'),
        (r'<p>Asigurare obligatorie și facultativă pentru locuința ta.</p>', r'<p data-i18n="ins_loc_p">Asigurare obligatorie și facultativă pentru locuința ta.</p>'),
        (r'<h4>Bunuri</h4>', r'<h4 data-i18n="ins_bun_t">Bunuri</h4>'),
        (r'<p>Protejează-ți bunurile valoroase împotriva riscurilor neprevăzute.</p>', r'<p data-i18n="ins_bun_p">Protejează-ți bunurile valoroase împotriva riscurilor neprevăzute.</p>'),
        (r'<h4>Călătorie</h4>', r'<h4 data-i18n="ins_cal_t">Călătorie</h4>'),
        (r'<p>Asigurare medicală de călătorie pentru vacanțe fără griji.</p>', r'<p data-i18n="ins_cal_p">Asigurare medicală de călătorie pentru vacanțe fără griji.</p>'),
        (r'<h4>Sănătate</h4>', r'<h4 data-i18n="ins_san_t">Sănătate</h4>'),
        (r'<p>Asigurări de sănătate pentru acces la cele mai bune servicii medicale.</p>', r'<p data-i18n="ins_san_p">Asigurări de sănătate pentru acces la cele mai bune servicii medicale.</p>'),
        (r'<h4>Viață</h4>', r'<h4 data-i18n="ins_viata_t">Viață</h4>'),
        (r'<p>Protecție financiară pentru tine și familia ta pe termen lung.</p>', r'<p data-i18n="ins_viata_p">Protecție financiară pentru tine și familia ta pe termen lung.</p>'),
        (r'<h4>Răspundere civilă</h4>', r'<h4 data-i18n="ins_rc_t">Răspundere civilă</h4>'),
        (r'<p>Acoperire pentru daunele produse terților în activitatea profesională.</p>', r'<p data-i18n="ins_rc_p">Acoperire pentru daunele produse terților în activitatea profesională.</p>'),

        (r'<span class="section-label">Cum funcționează</span>', r'<span class="section-label" data-i18n="hw_label">Cum funcționează</span>'),
        (r'<h2 class="section-title">Proces simplu, în 4 pași</h2>', r'<h2 class="section-title" data-i18n="hw_title">Proces simplu, în 4 pași</h2>'),
        (r'<p class="section-subtitle">\s*De la primul contact.*?\s*</p>', r'<p class="section-subtitle" data-i18n="hw_sub">\n          De la primul contact până la emiterea poliței sau aprobarea creditului, totul este simplu și transparent.\n        </p>'),

        (r'<h4>Contactează-mă</h4>', r'<h4 data-i18n="hw_s1_t">Contactează-mă</h4>'),
        (r'<p>Sună-mă sau scrie-mi pe WhatsApp pentru o discuție inițială gratuită.</p>', r'<p data-i18n="hw_s1_p">Sună-mă sau scrie-mi pe WhatsApp pentru o discuție inițială gratuită.</p>'),
        (r'<h4>Analizăm nevoile</h4>', r'<h4 data-i18n="hw_s2_t">Analizăm nevoile</h4>'),
        (r'<p>Identificăm împreună soluția optimă pentru situația ta specifică.</p>', r'<p data-i18n="hw_s2_p">Identificăm împreună soluția optimă pentru situația ta specifică.</p>'),
        (r'<h4>Primești oferta</h4>', r'<h4 data-i18n="hw_s3_t">Primești oferta</h4>'),
        (r'<p>Îți prezint cele mai bune oferte de pe piață, transparente și personalizate.</p>', r'<p data-i18n="hw_s3_p">Îți prezint cele mai bune oferte de pe piață, transparente și personalizate.</p>'),
        (r'<h4>Finalizăm rapid</h4>', r'<h4 data-i18n="hw_s4_t">Finalizăm rapid</h4>'),
        (r'<p>Emitere rapidă a documentelor, fără birocrație inutilă.</p>', r'<p data-i18n="hw_s4_p">Emitere rapidă a documentelor, fără birocrație inutilă.</p>'),

        (r'<span class="section-label">Creditare</span>', r'<span class="section-label" data-i18n="crd_label">Creditare</span>'),
        (r'<h2 class="section-title">Soluții de creditare</h2>', r'<h2 class="section-title" data-i18n="crd_title">Soluții de creditare</h2>'),
        (r'<p class="section-subtitle">\s*Găsim împreună.*?\s*</p>', r'<p class="section-subtitle" data-i18n="crd_sub">\n          Găsim împreună creditul cu cele mai avantajoase condiții, adaptat posibilităților tale.\n        </p>'),

        (r'<h3>Credit ipotecar</h3>', r'<h3 data-i18n="crd_ipo_t">Credit ipotecar</h3>'),
        (r'<p>Finanțare pentru achiziția locuinței visurilor tale, cu dobânzi competitive.</p>', r'<p data-i18n="crd_ipo_p">Finanțare pentru achiziția locuinței visurilor tale, cu dobânzi competitive.</p>'),
        (r'<li>Dobânzi avantajoase</li>', r'<li data-i18n="crd_ipo_l1">Dobânzi avantajoase</li>'),
        (r'<li>Perioade flexibile de rambursare</li>', r'<li data-i18n="crd_ipo_l2">Perioade flexibile de rambursare</li>'),
        (r'<li>Consultanță bancară completă</li>', r'<li data-i18n="crd_ipo_l3">Consultanță bancară completă</li>'),
        (r'<li>Suport în obținerea aprobării</li>', r'<li data-i18n="crd_ipo_l4">Suport în obținerea aprobării</li>'),

        (r'<h3>Refinanțare</h3>', r'<h3 data-i18n="crd_ref_t">Refinanțare</h3>'),
        (r'<p>Reduci rata lunară sau obții condiții mai bune pentru creditul existent.</p>', r'<p data-i18n="crd_ref_p">Reduci rata lunară sau obții condiții mai bune pentru creditul existent.</p>'),
        (r'<li>Reducerea costurilor lunare</li>', r'<li data-i18n="crd_ref_l1">Reducerea costurilor lunare</li>'),
        (r'<li>Consolidare credite multiple</li>', r'<li data-i18n="crd_ref_l2">Consolidare credite multiple</li>'),
        (r'<li>Negociere dobânzi</li>', r'<li data-i18n="crd_ref_l3">Negociere dobânzi</li>'),
        (r'<li>Analiză gratuită a situației</li>', r'<li data-i18n="crd_ref_l4">Analiză gratuită a situației</li>'),

        (r'<h3>Nevoi personale</h3>', r'<h3 data-i18n="crd_nev_t">Nevoi personale</h3>'),
        (r'<p>Credit rapid pentru proiectele tale personale, fără garanții imobiliare.</p>', r'<p data-i18n="crd_nev_p">Credit rapid pentru proiectele tale personale, fără garanții imobiliare.</p>'),
        (r'<li>Aprobare rapidă</li>', r'<li data-i18n="crd_nev_l1">Aprobare rapidă</li>'),
        (r'<li>Fără garanții imobiliare</li>', r'<li data-i18n="crd_nev_l2">Fără garanții imobiliare</li>'),
        (r'<li>Sume flexibile</li>', r'<li data-i18n="crd_nev_l3">Sume flexibile</li>'),
        (r'<li>Documente minime</li>', r'<li data-i18n="crd_nev_l4">Documente minime</li>'),

        (r'<span class="section-label">Testimoniale</span>', r'<span class="section-label" data-i18n="tst_label">Testimoniale</span>'),
        (r'<h2 class="section-title">Ce spun clienții</h2>', r'<h2 class="section-title" data-i18n="tst_title">Ce spun clienții</h2>'),
        (r'<p class="section-subtitle">\s*Opiniile celor.*?\s*</p>', r'<p class="section-subtitle" data-i18n="tst_sub">\n          Opiniile celor care au ales să lucreze cu mine.\n        </p>'),

        (r'<p>„A fost foarte ușor să închei polița RCA.*?\s*încredere!"</p>', r'<p data-i18n="tst_1_p">„A fost foarte ușor să închei polița RCA, totul s-a rezolvat rapid și fără bătăi de cap. Recomand cu\n            încredere!"</p>'),
        (r'<span>Client asigurări auto</span>', r'<span data-i18n="tst_1_c">Client asigurări auto</span>'),

        (r'<p>„Am primit cele mai bune oferte de pe piață pentru creditul ipotecar.*?\s*superlativ."</p>', r'<p data-i18n="tst_2_p">„Am primit cele mai bune oferte de pe piață pentru creditul ipotecar. Profesionalism și transparență la\n            superlativ."</p>'),
        (r'<span>Client creditare</span>', r'<span data-i18n="tst_2_c">Client creditare</span>'),

        (r'<p>„Inițial am avut reticențe.*?\s*pentru nevoile mele."</p>', r'<p data-i18n="tst_3_p">„Inițial am avut reticențe, dar Dragoș m-a ghidat cu răbdare prin tot procesul. Acum am asigurarea perfectă\n            pentru nevoile mele."</p>'),
        (r'<span>Client asigurări locuință</span>', r'<span data-i18n="tst_3_c">Client asigurări locuință</span>'),

        (r'<span class="section-label">FAQ</span>', r'<span class="section-label" data-i18n="faq_label">FAQ</span>'),
        (r'<h2 class="section-title">Întrebări Frecvente</h2>', r'<h2 class="section-title" data-i18n="faq_title">Întrebări Frecvente</h2>'),
        (r'<p class="section-subtitle">\s*Răspunsuri rapide.*?\s*</p>', r'<p class="section-subtitle" data-i18n="faq_sub">\n          Răspunsuri rapide la cele mai comune întrebări despre serviciile mele financiare.\n        </p>'),

        (r'<h4>Cât costă o consultanță financiară\?</h4>', r'<h4 data-i18n="faq_1_q">Cât costă o consultanță financiară?</h4>'),
        (r'<p>Consultanța inițială este 100% gratuită.*?\s*soluție de asigurare sau creditare.</p>', r'<p data-i18n="faq_1_a">Consultanța inițială este 100% gratuită. Începem prin a discuta nevoile tale pentru a găsi cea mai bună\n              soluție de asigurare sau creditare.</p>'),
        (r'<h4>Ce tipuri de asigurări poți intermedia\?</h4>', r'<h4 data-i18n="faq_2_q">Ce tipuri de asigurări poți intermedia?</h4>'),
        (r'<p>Colaborez cu numeroase companii de asigurări.*?\s*călătorie, sănătate, viață și malpraxis.</p>', r'<p data-i18n="faq_2_a">Colaborez cu numeroase companii de asigurări și te pot ajuta cu RCA, CASCO, PAD, asigurări de bunuri,\n              călătorie, sănătate, viață și malpraxis.</p>'),
        (r'<h4>Mă poți ajuta cu refinanțarea unui credit existent\?</h4>', r'<h4 data-i18n="faq_3_q">Mă poți ajuta cu refinanțarea unui credit existent?</h4>'),
        (r'<p>Sigur! Vom analiza contractul actual.*?\s*rată mai mică sau o perioadă optimizată de rambursare.</p>', r'<p data-i18n="faq_3_a">Sigur! Vom analiza contractul actual și vom identifica ofertele băncilor concurente pentru a obține o\n              rată mai mică sau o perioadă optimizată de rambursare.</p>'),
        (r'<h4>Cât durează procesul de emitere a unei polițe\?</h4>', r'<h4 data-i18n="faq_4_q">Cât durează procesul de emitere a unei polițe?</h4>'),
        (r'<p>Pentru polițele auto \(RCA/CASCO\) și de călătorie.*?\s*documentele necesare și validăm plata.</p>', r'<p data-i18n="faq_4_a">Pentru polițele auto (RCA/CASCO) și de călătorie, emiterea se face aproape instant, imediat ce primim\n              documentele necesare și validăm plata.</p>'),

        (r'<span class="section-label">Contact</span>', r'<span class="section-label" data-i18n="cnt_label">Contact</span>'),
        (r'<h2 class="section-title">Hai să discutăm</h2>', r'<h2 class="section-title" data-i18n="cnt_title">Hai să discutăm</h2>'),
        (r'<p class="section-subtitle">\s*Sunt mereu la un telefon distanță.*?\s*</p>', r'<p class="section-subtitle" data-i18n="cnt_sub">\n          Sunt mereu la un telefon distanță. Contactează-mă pentru o consultanță gratuită.\n        </p>'),

        (r'<h4>Telefon</h4>', r'<h4 data-i18n="cnt_p_t">Telefon</h4>'),
        (r'<h4>WhatsApp</h4>', r'<h4 data-i18n="cnt_w_t">WhatsApp</h4>'),
        (r'<p>Scrie-mi oricând pe WhatsApp</p>', r'<p data-i18n="cnt_w_p">Scrie-mi oricând pe WhatsApp</p>'),
        (r'<h4>Program</h4>', r'<h4 data-i18n="cnt_s_t">Program</h4>'),
        (r'<p>Luni – Vineri: 09:00 – 18:00</p>', r'<p data-i18n="cnt_s_p">Luni – Vineri: 09:00 – 18:00</p>'),
        (r'<h4>Locație</h4>', r'<h4 data-i18n="cnt_l_t">Locație</h4>'),
        (r'<p>România</p>', r'<p data-i18n="cnt_l_p">România</p>'),

        (r'<h3 style="font-size: 1.3rem; margin-bottom: 24px;">Trimite un mesaj</h3>', r'<h3 style="font-size: 1.3rem; margin-bottom: 24px;" data-i18n="frm_title">Trimite un mesaj</h3>'),
        (r'<label for="name">Numele tău</label>', r'<label for="name" data-i18n="frm_l_name">Numele tău</label>'),
        (r'placeholder="Ex: Ion Popescu"', r'placeholder="Ex: Ion Popescu" data-i18n="frm_p_name"'),
        (r'<label for="phone">Telefon</label>', r'<label for="phone" data-i18n="frm_l_phone">Telefon</label>'),
        (r'placeholder="Ex: 07xx xxx xxx"', r'placeholder="Ex: 07xx xxx xxx" data-i18n="frm_p_phone"'),
        (r'<label for="interest">Sunt interesat de</label>', r'<label for="interest" data-i18n="frm_l_int">Sunt interesat de</label>'),
        
        (r'<option value="" disabled selected>Alege un serviciu</option>', r'<option value="" disabled selected data-i18n="frm_opt_def">Alege un serviciu</option>'),
        (r'<option value="rca">Asigurare RCA</option>', r'<option value="rca" data-i18n="frm_opt_rca">Asigurare RCA</option>'),
        (r'<option value="casco">Asigurare CASCO</option>', r'<option value="casco" data-i18n="frm_opt_casco">Asigurare CASCO</option>'),
        (r'<option value="locuinta">Asigurare locuință</option>', r'<option value="locuinta" data-i18n="frm_opt_loc">Asigurare locuință</option>'),
        (r'<option value="calatorie">Asigurare călătorie</option>', r'<option value="calatorie" data-i18n="frm_opt_cal">Asigurare călătorie</option>'),
        (r'<option value="sanatate">Asigurare sănătate</option>', r'<option value="sanatate" data-i18n="frm_opt_san">Asigurare sănătate</option>'),
        (r'<option value="viata">Asigurare viață</option>', r'<option value="viata" data-i18n="frm_opt_via">Asigurare viață</option>'),
        (r'<option value="bunuri">Asigurare bunuri</option>', r'<option value="bunuri" data-i18n="frm_opt_bun">Asigurare bunuri</option>'),
        (r'<option value="rc">Răspundere civilă</option>', r'<option value="rc" data-i18n="frm_opt_rc">Răspundere civilă</option>'),
        (r'<option value="ipotecar">Credit ipotecar</option>', r'<option value="ipotecar" data-i18n="frm_opt_ipo">Credit ipotecar</option>'),
        (r'<option value="refinantare">Refinanțare</option>', r'<option value="refinantare" data-i18n="frm_opt_ref">Refinanțare</option>'),
        (r'<option value="nevoi">Credit nevoi personale</option>', r'<option value="nevoi" data-i18n="frm_opt_nev">Credit nevoi personale</option>'),
        (r'<option value="imobiliar">Consultanță imobiliară</option>', r'<option value="imobiliar" data-i18n="frm_opt_imo">Consultanță imobiliară</option>'),
        
        (r'<label for="message">Mesaj</label>', r'<label for="message" data-i18n="frm_l_msg">Mesaj</label>'),
        (r'placeholder="Scrie aici detaliile tale..."', r'placeholder="Scrie aici detaliile tale..." data-i18n="frm_p_msg"'),
        (r'✉️ Trimite mesajul\s*</button>', r'<span data-i18n="frm_btn">✉️ Trimite mesajul</span>\n            </button>'),

        (r'<p>\s*Dragoș Vîrjoghe — Consultant în asigurări.*?\s*</p>', r'<p data-i18n="ftr_desc">\n            Dragoș Vîrjoghe — Consultant în asigurări, creditare și imobiliar. Partenerul tău de încredere pentru\n            soluții financiare personalizate.\n          </p>'),
        (r'<h4>Navigare</h4>', r'<h4 data-i18n="ftr_nav">Navigare</h4>'),
        (r'<h4>Asigurări</h4>', r'<h4 data-i18n="ftr_asig">Asigurări</h4>'),
        (r'<h4>Creditare</h4>', r'<h4 data-i18n="ftr_cred">Creditare</h4>'),
        (r'<p>&copy; 2026 Dragoș Vîrjoghe\. Site realizat cu pasiune de către <a href="https://echipadetocilari\.ro"\s*target="_blank">Echipa de Tocilari</a></p>', r'<p data-i18n="ftr_cp">&copy; 2026 Dragoș Vîrjoghe. Site realizat cu pasiune de către <a href="https://echipadetocilari.ro"\n            target="_blank">Echipa de Tocilari</a></p>'),
    ]

    for search, replace in replacements:
        content = re.sub(search, replace, content)
    
    # insert the translations script and UI switcher in index.html
    # switcher in navbar:
    switcher = r'''<div class="lang-switch" id="langSwitch">
        <span class="active" data-lang="ro">RO</span>
        <span class="separator">|</span>
        <span data-lang="en">EN</span>
      </div>'''
    
    content = re.sub(r'(<div class="menu-toggle" id="menuToggle">)',  switcher + r'\n      \1', content)
    
    # insert script tag at the bottom
    content = re.sub(r'(<script src="script.js"></script>)', r'<script src="translations.js"></script>\n  \1', content)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
