## Dokumentacija  za projekat iz Dinamičkih web sistema
### Tema projekta: Candy Crush Saga
### Profesor: prof.dr Adis Alihodžić
### Student: Imran Sobo
### Indeks: 90/IT-19

#### Struktura aplikacije : 
- Aplikacija je podijeljena na backend i frontend.
- U folderu candy_api se nalazi Django aplikacija.
- U folderu candy-crush-saga-imran-sobo se nalazi React aplikacija.
- Korištene tehnologije i biblioteke: 
	-  React.js
	-  Django
	-  Bootstrap i CSS
	-  npm paket SweetAlert2
	- npm paket CountdownTimer
	- npm paket axios za slanje HTTP zahtjeva i primanje response-a
	
## Backend tehnologija - Django

### O Djangu
Django je web-framework koji prati model-template-views arhitekturu (MTV). Zasnovan je na Pythonu te posebno naglašava ponovno iskorištavanje koda kao i brzo razvijanje aplikacije. Django je besplatan, open-source i ima dobro razvijenu dokumentaciju. Ključni mehanizmi kod razvijanja web-aplikacije u Djangu su :
- urls (fajl u kojem se nalaze sve rute s kojima pravimo REST API)
- views (fajl u kojem se nalaze klase i metode koje primaju HTTP zahtjeve te vraćaju HTTP respons-ove
- modeli (modeli su u suštini instance klasa koje nam služe za pravljenje tabela i baze podataka) 


##### Tabele
Za razvoj backenda je korišten Django koji u pozadini koristi SQLite bazu. Za pravljenje tabela u Djangu je nasljeđena klasa Model te su razvijene sljedeće dvije klase: Player i Score. Model Player omogućava registraciju korisnika kao i login. 
Model Player ima tri polja/atributa, a to su: player_name, email, password.
Model Score sadrži dva polja/atributa, a to su: player koji je strani ključ te score koji je IntegerField.	
##### Serializeri
Serializeri općenito dozvoljavaju da se kompleksni tipovi podataka poput querysetova ili instanci modela pretvore u Pythonove tipove podataka koji se onda mogu renderati kao JSON, XML ili drugi tipovi.
U projektu su korištena 3 serializera, a to su:
- PlayerListSerializer - vraća polja:  'id', 'player_name', 'email', 'password'.
- ScoreListSerializer - vraća polja: 'id', 'player', 'score'.
- ScoreBoardSerializer - vraća ista polja kao ScoreListSerializer, ali ima atribut depth koji treba biti tipa int te označava broj veza kroz koje treba proći prije nego se vrati JSON objekat. Tačnije gleda u koliko je veza model sa nekim drugim modelima, te na taj način vraća stvarne vrijednosti iz tih veznih tabela, a ne samo ID-eve.


##### Rute
Kako bi svi prijašnji koncepti imali smisla, potrebno je napraviti rute koje "gađamo" sa frontenda. Ove rute pravimo u urls.py fajlu. To su sljedeće rute:
- path('player/', views.PlayerList.as_view()) - ova ruta omogućava pristup podacima svih igrača. 
- path('login', views.user_login) - ova ruta odrađuje login
- path('scores/', views.ScoreList.as_view()) - omogućava unos skora jednog igrača
- path('scoreboard/', views.ScoreBoard.as_view()) - izlistava skorove svih igrača
- path('player/<int:pk>', views.PlayerDetails.as_view()) - vraća detalje određenog igrača, tj. po ID-u.
- path('forgot-password', views.reset_user_pass) - ova ruta omogućava reset lozinke igrača.
Ove metode ću opisati u idućoj sekciji.

##### Views (metode)

- class PlayerList -  ova klasa upitom prolazi kroz model Player i vraća sve igrače pomoću serializera PlayerListSerializer.
- class  ScoreList -  ova klasa upitom prolazi kroz model ScoreList i vraća sve scorove  pomoću serializer ScoreListSerializer.
- class  ScoreBoard - ova klasa upitom prolazi kroz model ScoreList ali vraća scorove od najvećeg ka najmanjem pomoću order_by().
- class PlayerDetails - ova klasa upitom prolazi kroz model Player ali vraća detalje tačno jednog igrača.
- def user_login - ova metoda provjerava login na način da iz requesta uzme email i password igrača te upitom prođe kroz tabelu Player. Ukoliko pronađe igrača, sa JsonResponse-om će vratiti true i detalje tog igrača te omogućiti mu login i igranje igrice. U suprotnom, igraču neće biti dozvoljeno da se uloguje.
- def reset_user_pass - ova metoda iz requesta uzima email igrača te prolazi kroz model Player, ako nađe tog korisnika, generiše mu novu lozinku te spasi je, u suprotnom na frontend vraća response koji označava da korisnik ne postoji u bazi podataka. Nova lozinka korisniku dolazi na email. Slanje lozinke na email je implementirano pomoću ugrađenog mehanizma za slanje emaila koji se zove send_mail().	




## Frontend tehnologija - React.js

### O React.js
React.js je besplatna i open-source JavaScript biblioteka namijenjena za frontend, tj. pravljenje korisničkog interfejsa koji je zasnovan na komponentama. Komponente su ključni koncept u React.js, omogućavaju da se kod manje kopira te dobija se na preglednosti i čitljivosti koda. Komponente mogu biti: funkcionalne komponente i komponente zasnovane na klasama. U ovom projektu su korištene funkcionalne komponente. Velika korist se dobija iz kuka (eng. hooks) koje omogućavaju korisnicima dinamički razvoj stranice. To se ogleda u korištenju kuke poput useState(), koja omogućava postavljanje novih vrijednosti, novog stanja i sl. Bitno je spomenuti i kuku useEffect() s kojom je moguće odraditi mnoge stvari pri samom učitavanju tj. renderu komponente.

Komponente se nalaze u posebnom folderu **components**.
U nastavku ću opisati funkcije svake komponente te njene metode.
Korištene su sljedeće komponente: 
- About.js
- ChangePassword.js
- ForgotPassword.js
- Header.js
- Home.js
- Igrica.js
- Login.js
- Logout.js
- Main.js
- Register.js
- Score.js
- ScoreList.js

	### About.js
	U komponenti About.js su navedene osnovne informacije o projektu, studentu te predmetu. Iskorištena je useEffect() kuka kako bi se dinamički promijenio naslov stranice te tabele za prikaz informacija o predmetu.
  ### ChangePassword.js
  U komponenti ChangePassword.js se vrši promjena lozinke na način da se dobavi stara lozinka pomoću useEffect() tj. pri učitavanju komponente te korisnik ima opciju unosa nove lozinke koju mora dva puta unijeti kako bi je potvrdio. U slučaju da lozinke nisu identične, ne dozvoljava se promjena. U suprotnom, pomoću  varijable 
  const  BASE_URL = "http://127.0.0.1:8000/api"; se vrši PUT metoda sa axiosom gdje se na bazni url nadovezuje '/player/' te ID trenutnog igrača koji se dobija iz local storage-a sljedećom linijom koda: const  playerId = localStorage.getItem("playerId");
 Bazni url postaje npr. http://127.0.0.1:8000/api/player/1. Axios HTTP zahtjev je potrebno umotati u try-catch blok kako bi uspjeli uhvatiti eventualne izuzetke.


  ### ForgotPassword.js
  U komponenti ForgotPassword.js se vrši generisanje nove lozinke u slučaju da je korisnik zaboravio lozinku. Korisnik treba unijeti svoj email koji se sa axios post metodom šalje na backend, gdje se na ruti http://127.0.0.1:8000/api/forgot-password uzima taj email iz requesta te upitom provjerava da li taj korisnik postoji u bazi podataka. Ukoliko postoji, generiše mu se nova lozinka od 8 nasumičnih znakova i spašava se te se šalje na korisnikov email. U suprotnom, na backendu se baca izuzetak kako korisnik ne postoji te se na frontend vraća JsonResponse koji naznačava da korisnik ne postoji u bazi podataka.

  ### Footer.js
  Komponenta Footer.js sadrži sadrži JSX element **footer** te container. U njemu se nalazi link za vraćanje na vrh stranice.

  ### Header.js
  Komponenta Header.js ustvari predstavlja dinamički Navbar.
  U Navbaru se nalaze Linkovi na komponente: Početna, O Projektu, Scoreboard, Login, Register, Igrica, Uredi profil te Logout.
  U slučaju da korisnik nije ulogovan, može vidjeti samo Linkove na Početnu, O projektu, Login, Register te Scoreboard. Igricu nije moguće igrati u slučaju da korisnik nije ulogovan. To je postignuto pomoću logičkih varijabli te uslovnog renderovanja na sljedeći način: 
  **const  playerLoginStatus = localStorage.getItem("playerLoginStatus");
  {  playerLoginStatus === "true" &&
  < Link  className="nav-link mt-3"  arica-current="page"  to="/logout">Logout</ Link>
 }**
  

  ### Home.js
  U komponenti Home.js se prikazuje početna stranica. U slučaju da korisnik nije ulogovan, prikazuje mu se stranica koja ga navodi da se registruje/uloguje. Ako je ulogovan ima mogućnost pokretanja igrice sa početne stranice. Opet se koristi: 
  const  playerLoginStatus = localStorage.getItem("playerLoginStatus");
i uslovno se provjerava status korisnika i u zavisnosti od toga mu se prikazuje odgovarajući sadržaj.


   ### Igrica.js
   Komponenta Igrica.js ujedno predstavlja najbitniju komponentu u projektu u kojoj se nalazi logika igrice. U nastavku slijedi opis metoda i logike u komponenti:
   - const [gameScore, setGameScore] = useState(0);
	   - koristi se za postavljanje skora u igrici.
   - const [dragObjekat, setDragObjekat] = useState(null)
    	- koristi se za povlačenje bombone koju želimo pomjeriti.
   - const [promijeniObjekat, setPromijeniObjekat] = useState(null)
	   - koristi se za mijenjanje starog objekta na novi, ukoliko je potez validan.
   - const [trenutneBoje, setTrenutneBoje] = useState([]);
		- u nizu trenutneBoje se nalazi trenutni aranžman boja koji se mijenja nakon svakog poteza.

	**Metoda kombinacijaCetiriKolona()** 
	Ova metoda koristi brojačku petlju od 0 do 39. Petlja ide do broja 39 jer je matrica formata 8x8 pa nema smisla provjeravati indekse iznad 39. U petlji se provjerava da li za neki i-ti element postoji kombinacija od 4 ista elementa. Koordinate tih elemenata su navedene u nizu **const  kolonaSaCetiri = [i, i+SIRINA, i+SIRINA*2, i+SIRINA*3];**
	U petlji se if-strukturom provjerava da li za i-ti element važi da su navedene vrijednosti jednake trenutnoj vrijednosti. Ukoliko je navedeni uslov tačan, pomoću useState se poveća stari skor za +4 te metoda vraća true, u suprotnom false. 

	**Metoda kombinacijaCetiriRed()**
	Ova metoda koristi brojačku petlju koja ide od 0 do 64 jer se provjerava za svaki red za moguću kombinaciju. U petlji se neće provjeravati neodgovarajući indeksi. Neodgovarajući indeksi su:  [5,6,7,8,13,14,15,21,22,23,29,30,31,37,38,39,45,46,47,53,54,55,62,63,64]
	 Kombinacija se traži na sljedeći način:
	**const  redSaCetiri = [i, i+1, i+2, i+3];**
Ukoliko je svaki element iz niza redSaCetiri jednak trenutnom, to znači da je pronađeno poklapanje te se sa useState povećava stara vrijednost za +4 i metoda vraća true, u suprotnom vraća false.

	**Metoda kombinacijaTriKolona()**
	Ova metoda koristi brojačku petlju koja ide od 0 do 47 jer za matricu formata 8x8 ima smisla provjeravati samo indekse do tog broja. Elementi koji se provjeravaju su:
	**const  kolonaSaTri = [i, i+SIRINA, i+SIRINA*2];**
	Ukoliko su elementi niza međusobno jednaki te jednaki sa trenutnim (i-tim) elementom, sa useState se povećava stara vrijednost za +3 te metoda vraća true, u suprotnom false.

	**Metoda kombinacijaTriRed()**
	Ova metoda koristi brojačku petlju koja ide od 0 do 64 i provjerava sve elemente osim neodgovarajućih indeksa, tj. indeksa za koje nema validne kombinacije. 
	Elementi koji se provjeravaju su:
	**const  redSaTri = [i, i+1, i+2];** 
	Neodgovarajući indeksi su u ovom slučaju: [6,7,14,15,22,23,30,31,38,39,46,47,54,55,63,64].
	Ukoliko je svaki element iz niza redSaTri jednak trenutnom, to znači da je pronađeno poklapanje te se sa useState povećava stara vrijednost za +3 i metoda vraća true, u suprotnom vraća false.

	**Metoda popuniPraznaPolja()**
	Ova metoda petljom prolazi kroz matricu i traži prazna polja koja su nastala usljed uklanjanja kombinacija od 3 ili 4. Ukoliko se naiđe na prazno polje, linijama :
		**let  rand = Math.floor(Math.random() * candyBoje.length)
		trenutneBoje[i] = candyBoje[rand]**
	se omogućava da se prazno polje zamijeni novom bombonom.

	**Metoda dragStart(e)**
	Ova metoda se koristi za postavljanje elementa koji trenutno vučemo mišem sljedećom linijom:
	setDragObjekat(e.target)
	   

	**Metoda dragDrop(e)**
	Ova metoda se koristi za mijenjanje elementa sljedećom linijom: 
	setPromijeniObjekat(e.target)

	**Metoda dragEnd(e)**
	U ovoj metodi se na indeks ciljnog polja postavlja element koji smo vukli, tj. dragObjekat.
	**const  dozvoljeniPotezi = [dragPoljeId - 1, dragPoljeId - SIRINA, dragPoljeId + 1,dragPoljeId + SIRINA]**
	**const  jeLiKolonaCetiri = kombinacijaCetiriKolona()
	const  jeLiRedCetiri = kombinacijaCetiriRed()
	const  jeLiKolonaTri = kombinacijaTriKolona()
	const  jeLiRedTri = kombinacijaTriRed()**

	Ukoliko indeks ciljnog polja nije dozvoljen, tj. idemo izvan opsega , polje koje smo vukli se vraća na staro, tj potez nije dozvoljen.
	U suprotnom, objekat će se promijeniti, te u zavisnosti od toga koja metoda je vratila true, povećava se score za 3 ili 4.

	**Metoda napraviTablu()**
	Metoda napraviTablu for petljom pravi matricu od 64 nasumična elementa, odnosno bombone i postavlja trenutni aranžman boja na tu matricu linijom: **setTrenutneBoje(sveRandomBoje);**
	Ova metoda se poziva u useEffect() kako bi se matrica napravila pri učitavanju stranice.

	**Metoda postScore()**
	Metoda postScore se poziva nakon što se pozove metoda onComplete() iz Timera.
	Ova metoda uzima trenutni skor igrača, njegov username te radi axios HTTP zahtjev za unos skora tog igrača.



### Login.js
U komponenti Login.js se vrši slanje zahtjeva za login igrača. Šalje se axios HTTP zahtjev na backend rutu : "http://127.0.0.1:8000/api/login"; na kojoj se poziva metoda **user_login()**. Ukoliko navedena metoda kroz JsonResponse vrati true, korisniku se odobrava pristup igrici i u localStorage se postavlja njegov ID i username, u suprotnom prikazuje mu se odgovarajuća poruka.





### Main.js
U komponenti Main.js se nalaze sve komponente frontend dijela aplikacije. Fiksirane komponente, tj. komponente koje se stalno prikazuju su Header i Footer dok se sa < Routes > iz react-router-dom-a provjeravaju rute te vrši preusmjeravanje


### Register.js
Komponenta Register.js sadrži formu u koju unosi svoj username, email te lozinku. Pravi se axios HTTP zahtjev koji šalje podatke na backend kroz instancu FormData(). Ukoliko neki od podataka nije validan, ne dozvoljava mu se registracija. U suprotnom, korisnik se registruje te preusmjerava na login komponentu.

### Score.js
Komponenta Score.js kao props prima skor te sadrži samo broj koji predstavlja varijabla score iz komponente Igrica.js te ova komponenta služi samo za prikazivanje trenutnog skor-a.

### ScoreList.js
Komponenta ScoreList.js sadrži tabelu sa skorovima svih igrača. Pristup ovoj komponenti imaju svi korisnici, neovisno o tome da li su ulogovani. Ukoliko su korisnici ulogovani i pristupe ovoj komponenti, a nalaze se na listi skorova, njihova imena će biti obojana plavom bojom. Navedena stavka se postiže sa uslovnim renderovanjem.
  
