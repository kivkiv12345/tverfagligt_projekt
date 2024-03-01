
## Læsevejledning

- ORM (Object Relational Mapping)
- API (Application Programming Interface)
- SQL (Structured Query Language)
- Repo ((GitHub) repository)
- DRF (Django-REST-Framework)


## Kravspecifikation

### Definition af produktet

### Funktionalitet

### Begrænsning

### Testkonditioner


## Brugervejledning

### Installation


 Pakker anbefalet til installation og opsætning

- Docker (version ^25.0.3, som bør inkludere Docker Compose)
- Git
- Python 3 (version ^3.10)
- Flutter / Dart


Docker Compose anbefales til opsætningen af systemet, hvilket tillader at alle tjenester startes med én enkelt kommando.
Installationproceduren for Docker varirer afhængt af installationsdestinationens platform, derfor bedes administratoren følge Dockers officielle guide, fundet her:
https://docs.docker.com/engine/install/

Projektets afhængigheder afhænger af tilpas nye "Docker Compose" funktionaliter, som kun kan findes når kommandoen køres som "docker compose" og __ikke__ "docker-compose".


Opsættes systemet på Ubuntu, kan følgende kommandoer som udgangspunkt anvendes til installationen af afhængigheder:


    # Docker

    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin


    # Git

    sudo apt install git

Herefter anvendes følgende kommandoer til at hente og starte programmet:

    git clone https://github.com/kivkiv12345/tverfagligt_projekt.git

    cd tverfagligt_projekt

    # Her forventes det at start af Flutter webserveren kan tage lang tid.
    docker compose up



### Anvendelse

#### Django Admin

Django kommer med en nem tilpasselig administrationsside som en del af deres contrib side.
Django applikationen implementerer derfor denne administrationsside, for at afprøve og understøtte udviddet funktionalitet som endnu ikke findes i Flutter applikationen, såsom oprettelse af nye servere.

Køres projektet lokalt kan administrationssiden findes på 127.0.0.1:8000/admin

### Service

Se afsnittet "Regristrering af spil / Manager klasser" for understøttelse af flere spil.

## Teknisk produktdokumentation

Dette afsnit dækker væsentlige elementer for systemets nuværende implementation, samt mulige udvidelser og refaktoring dertil.

### Docker

Docker er et meget veletableret virtualiserings værktøj.
Docker adskiller sig fra typiske virtualiserings værktøjer ved ikke at bruge virtuelle maskiner, i virkeligheden separerer Docker bare processer ved at bruge namespaces.

Docker anvendes til at forenkle opsætningen af system, og samtidigt også gøre det nemt at slette bagefter.
Django applikationen er bygget således at spilservere skulle kunne drives af vilkårlige teknologier, men på nuværende tidspunkt forkommer "Docker Compose" som den eneste konkrete implementation.
Hermed kræves det at Docker er installeret på serveren.

### Django

Som backend framework bruger projektet Django, som er et Python web framework med fokus på hurtig udvikling med indbygget sikkerhed.
Det primære formål med projektets Django backend er at tilbyde et web-API som muliggør at administrere spilserverne fra Flutter applikationen. Derfor skal backenden også tilbyde et fælles interface til diverse implementationer af spilservere.

Rodmappen for Django applikationen (i forhold til projektets rodmappe) findes i ./backend/
Stier forklaret i dette afsnit, tager derfor udgangspunkt i denne mappe.

Når man laver et Django projekt, laver men deri efterfulgt en (eller flere) "app(s)", hvori alt implementation forgår. Der findes ingen fast afgrænsning for hvad én app må indeholde, og hvornår projektet skal implementers på tværs af flere apps.

#### Regristrering af spil / Manager klasser

Projektets Django applikation adskiller sig fra typiske Django eksempler med Manager klassernes arvehierarki. Her registreres AbstractGameServerManager konkrete underklasser automatisk, hvorefter det nye spil, også automatisk, bliver en valgmulighed for brugere når de laver deres servere.

```
Bemærk dog at nye valgmuligheder for spil (konkrete AbstractGameServerManager underklasser) kræver en opdatering til databasen!
For at udføre denne opdatering manuelt benyttes følgende kommandoer:

python3 ./manage.py makemigrations
python3 ./manage.py migrate

Benytter man Docker eller "Docker Compose" udføres disse kommandoer automatisk, som set nederst i ./Dockerfile
```

Manager klasserne er derfor ansvarlige for at implementere den endegyldige forretningslogik angående håndtering af spilservere.
I et typisk Django projekt ligger den endegyldige forretningslogik direkte på databasemodellerne (hvor meget typisk ligger i Model.save()).
Den fordeling er ulempelig her, da den kræver kobling til konkrete nedarvede spilklasser (mht. forespørgsler til databasen).
Alternativt kan man i fremtiden refaktorere databasemodellerne til at bruge pakken Django-Polymorphism, i stedet for brugen af Manager klasserne. Brugen Django-Polymorphism tillader forespørgsler på abstrakte superklasser, som dermed tillader løs kobling. Bemærk dog at dette kan medføre værere ydeevne, da hver konkret spilklasse kræver én yderligere SQL JOIN i forespørgslerne.

Som den første konkrete spilklasse understøtter projektet servere til spillet Vintage Story, som i baggrunden kører vha. Docker-Compose. Men med Manager klassernes arvehierarki, kan udvikleren nemt udskifte hvordan spilserveren i virkeligheden køres. Som eksempel på hvordan én konkret underklasse kan se ud, vises VintageStoryManager nedenunder:

```
class VintageStoryManager(GitHubVersionedDockerComposeManager):
    #compose_file = 'docker-compose/vintage-story_server/docker-compose.yml'
    compose_file = 'repos/docker-vintagestory/docker-compose.yml'
    version_commit_map = {
        'newest': 'master',
        '1.19.3': '5ce36b8a75e909fa30bfdca9f20a2ac46000fdbf',
        '1.19.2': '71fab0d025eecbd73884be8dedced5c65226298d',
        '1.18.15': 'dd4818b90f74786442f7d1985bcb644915d884c1',
        '1.18.1': '558e4aa364a38f1ea8af1caf32c4f94240bfba1a',
    }
    repo = 'https://github.com/Devidian/docker-vintagestory.git'
    services = ['vsserver-local',]

    game_versions = (
        'newest',
        '1.19.3',
        '1.19.2',
        '1.18.15',
        '1.18.1',
    )
```

Klassen defineres udelukkende med klassevariabler som kræves af superklasserne, som hermed håndterer registrering og metoder.
Set her er kravene som følgende:

- VersionedGameServerManager
    - game_versions: Sequence[str]
- GitHubVersionedManager
    - version_commit_map: dict[str, str]
    - repo: str
- AbstractDockerComposeGameServerManager
    - compose_file: str
    - services: list[str] | str

```
Bemærk af konkrete underklasser skal defineres i filer som indlæses af Django under opstart, derfor er VintageStoryManager defineret i ./api/apps.py
```

#### Oprettelse og vedligeholdelse af web-API endpoints

Endpoints defineres i filen ./api/views.py og regristeres med dekoratoren @api_view(), hertil angives hvilke HTTP forspørgelesemetoder endepunktet skal acceptere.

Endepunktet synliggøres ved at specificere et, eller flere, URL som skal bruge det.
Det gør man i urls.py filen tilsvarende til sin app, til projektet her er det ./api/urls.py

Denne fil skal indeholde en variablen navngivet "urlpatterns" af typen list[path]:

```
from django.urls import path
from api.views import stop_server

urlpatterns = [
    # ...
    path(f"stop-server/", stop_server, name="stop-server"),
    # ...
]
```

Bemærk at "path"s constructor første argument er stien som skal føre til ens endepunkt/view, og derefter funktionen/klassen selv (class based view eksisterer også, men er ikke brugt i projektet her).
Typisk angiver man også et "name=" til sit URL/view. Herefter kan man omdiregere til navnet på sit URL/view, og derfor flytte dets placering efter behov.

Argumenter til endepunktet håndteres typisk forskelligt afhængigt af om man laver et GET eller POST  endpoint:

- POST: Argumenter hertil modtages typisk som JSON i kroppen af HTTP forespørgslen. Følgende signature viser hvordan argumenter til endepunktet kan findes i request.data:

```
    @api_view(['GET'])
    def is_server_running(request: Request) -> Response:
        print(request.data)
```

- GET: Til GET endepunkter laves argumenter typisk i URLet (som forspørgelsesargumenter).
Følgende path viser hvordan forspørgelsesargumenter registreres samtidigt med selve URLet til ens endepunkt i ./api/urls.py, hvor argumentet er angivet som \<str:ident>:

```
path(f"get-server-version/<str:ident>", get_server_version, name="get-server-version")
```

Hermed genererer (DRF) Django-REST-Framework en webside hvor man kan afprøve sit endpoint.
Denne webside kan tænkes som en simpel version af Swagger, da den ikke har kendskab til endepunktet accepterede argumenter (det er man selv ansvarlig for at dokumentere).

Heldigvis præsenterer DRF endepunkt funktionernes dokumentationstreng som dokumentation, hvilket vil sige at hvis man laver en multilinje streng straks efter funktionens signatur, bliver den præsenteret til brugere af web-APIet:

    @api_view(['GET'])
    def get_server_version(request: Request, ident: str) -> Response:
        """

        Expected JSON:
        {
            "server_ident": int | str,
        }
        """

#### Nuværende struktur på endpoints

Den typiske struktur til Django applikationens web-API er som følgende:

1. Validér argumenter
2. Find efterspurgte server
3. Tjek tilladelser
4. Kald efterspurgte GameServerManager funktion

Hermed menes der at typiske spilserver forespørgsler er implementeret som selvstændige funktioner på Manager klasserne.


#### Django Admin

Django's administrationsside kan nemt tilpasses med udviddet funktionalitet.


##### Admin actions

Som et simpelt eksempel kan man lave "action"s, som tillader udførelse at komplekse på mange server (model instanser) samtidigt. Definerer man den funktion man vil køre (brugen af dekoratoren "@admin.action()" anbefales, men er ikke nødvendig):

```
@admin.action(description="Start servers")
def start_servers(modeladmin: ModelAdmin, request: Request, queryset: QuerySet[GameServer]):
    for server in queryset:
        server.manager.start()
```

Argumentet "queryset" er de valgte instanser på listen af sine modeller (servere), som brugeren ønsker handlingen udført på.

Herefter registrerer ens "action" på admin klassen tilsvarende ens model:

```
class GameServerAdmin(ModelAdmin):
    model = GameServer
    ...
    actions = (..., start_servers, ..., )
    ...
```

Med følgende eksempel kan man herefter starte mange servere samtidigt på administratorsiden.


##### Simple ændringer til administratorsiden

Administratorsiden er opbygget med serverbaseret rendering, hvormed brugerændringer som udgangspunkt forekommer i Python, fremfor HTML.

Mærkværdigt er det faktum at det ikke nødvendigvis er alle spilserverklasser som kan håndtere versionering, derfor håndteres dette på administratorsiden med betinget rendering af ændringsformen. Metoden GameServerAdmin.get_form() viser hvordan spilklasser som ikke nedarver fra VersionedGameServerManager præsenteres uden versionering:

```
def get_form(self, request, obj: GameServer = None, change=False, **kwargs):
    
    ...

    class GameServerAdminForm(ModelForm):
        if isinstance(obj.manager, VersionedGameServerManager):
            CHOICES = ((game_version, game_version) for game_version in obj.manager.available_versions)
            server_version = forms.ChoiceField(choices=CHOICES, initial=obj.server_version)
        server_running = forms.BooleanField(initial=obj.manager.server_running(), required=False)

        ...

    return GameServerAdminForm
```

### Flutter

Programmet præsenteres af Flutter, som er et cross-platform frontend framework, hvormed den samme kode derfor kan præstere på: mobil, computere, web, mm.
Kører man systemet med Docker, kan Flutter tilgås som en webapp på port 8080.

Login proceduren fungere ved at Flutter sender de indtastede legitimationsoplysninger (brugernavn og kodeord) til Django applikationen, som derefter verificerer oplysningerne.
Herefter svarer Django applikationen med "Token" som Flutter applikationen efterfølgende bruger til at verificere brugeren identitet til forespørgsler.

Flutter applikationen bruger pakken shared_preferences til at persitere brugernavn og token til disken på tværs af sessioner. Hermed behøver brugere, som adgangspunkt, kun at logge ind én enkelt gang.


Flutter applikationen gør stort brug af pakken Bloc til at håndtere opdateringer af brugerfladen.
Disse opdateringer indebærer på nuværnde tidspunkt:
- Bemyndigelse af brugere ved login/logout.
- Ændring mellem mørkt og lyst tema.
- Ønskede og reelle opdateringer af servere (start/stop osv.)

En 'Bloc' er en kombineret state maskine og observer pattern. Brugere af en Bloc kan skabe 'Events' som kan påvirke den aktuelle Bloc instans til at skifte tilstand ("state"). Denne tilstand udsendes herefter til relevante lyttere (BlocBuilder instanser), som genbygger dele af brugerfladen baseret på informationen inkluderet i den udsendte tilstand instans.
Brugerfladen mest simple eksempel ses i form af ThemeBloc:

```
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class ThemeBloc extends Bloc<ThemeMode, ThemeMode> {

  ThemeBloc(super.initialState) {
    on<ThemeMode>(themeChange);
  }

  void themeChange(ThemeMode theme, Emitter<ThemeMode> emit) {
    emit(theme);
  }
}
```

Denne Bloc klasse bruger både ThemeMode klassen som 'events' og 'states', hermed behøver Bloc'en blot videresende det modtagede 'event' til lyttende BlocBuilder instanser:

```
BlocBuilder<ThemeBloc, ThemeMode>(
    builder: (context, themeMode) {
        return MaterialApp(
        ...
        themeMode: themeMode,
        home: const MyHomePage(title: 'Flutter Demo Home Page'),
        );
    },
),
```

I det overstående eksempel er themeMode argumentet den videresendte ThemeMode fra vores ThemeBloc. Hermed bygges resten af applikationen med det signalerede tema.
Temaet signaleres når brugeren trykker på følgende ListTile:


```
ListTile(
    title: Text('Dark Mode'),
    trailing: Switch(
        ...,
        onChanged: (value) {
            // Toggle dark mode
            ThemeMode newThemeMode =
                value ? ThemeMode.dark : ThemeMode.light;
            ...
            BlocProvider.of<ThemeBloc>(context).add(newThemeMode);
        },
    ),
),
```

Switch.onChanged() finder den nærmeste overstående ThemeBloc i widget træet, og giver den et event om at ændre temaet til det modsatte af den nuværnde.

### Database

Systemet bruger på nuværende tidspunkt én enkelt SQLite database, for at mindske kompleksiteten.
Takket været Django's ORM, kan databasen nemt ændres til et mere skalérbart alternativt efter behov.
Ønskes en PostgreSQL database, kan følgende ændreringer anvendes:

- Ændre "DATABASES" i ./backend/settings.py til:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
```

- Tilføj service til docker-compose.yml:
```
services:
    ...
    db:
    image: postgres
    volumes:
      - ./db_volume/db:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"  # Forward the port, so we can use the container when running Django locally for debug purposes.
    ...
```

### Diagrammer, beregninger, hardware, software m.v.

### Testrapport 


## Ordliste


## Kildehenvisninger


## Bilag
