
## Læsevejledning

- ORM (Object Relational Mapping)
- API (Application Programming Interface)
- SQL (Structured Query Language)
- Repo ((GitHub) repository)


## Kravspecifikation

### Definition af produktet

### Funktionalitet

### Begrænsning

### Testkonditioner


## Brugervejledning

### Installation

#### Pakker anbefalet til installation og opsætning

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

### Service


## Teknisk produktdokumentation

### Docker

Docker er et meget veletableret virtualiserings værktøj.
Docker adskiller sig fra typiske virtualiserings værktøjer ved ikke at bruge virtuelle maskiner, i virkeligheden separerer Docker bare processer ved at bruge namespaces.

Docker anvendes til at forenkle opsætningen af system, og samtidigt også gøre det nemt at slette bagefter.
Django applikationen er bygget således at spilservere skulle kunne drives af vilkårlige teknologier, men på nuværende tidspunkt forkommer "Docker Compose" som den eneste konkrete implementation.
Hermed kræves det at Docker er installeret på serveren.

### Django



### Flutter

### Diagrammer, beregninger, hardware, software m.v.

### Testrapport 


## Ordliste


## Kildehenvisninger


## Bilag
