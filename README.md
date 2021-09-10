# L.E.S.D. (LAG Event Shift Dispenser)
Manager de turnos para eventos organizados por LAG.

## Dependencias

Se hace uso de la api de python [telebot](https://pypi.org/project/pyTelegramBotAPI/) y del conector [mariadb-connector-python](https://github.com/mariadb-corporation/mariadb-connector-python)


## Set-up

### Instalar dependencias

En una maquina con python instalado ejecutaremos 

```bash
pip install pyTelegramBotAPI
```

```bash
pip install mariaDB
```

### Base de datos

Este bot utiliza MariaDB como su base de datos, así que para ello tendremos que instalar un servidor de MariaDB en el algún equipo, bien en el mismo que ejecute el bot o bien en otro que permita acceso al bot

Para que el boy funcione se necesita una base de datos con unas tablas concretas, para ver la estructura de la base de datos referir a los archivos de [database](./src/db).

Para crear a los administradores se ejecutará el siguiente comando:

```sql
INSERT INTO Admins (username) VALUE (NombreDeUsuario);
```

O en caso de que haya varios:

```sql
INSERT INTO Admins (username) VALUES (NombreDeUsuario1), (NombreDeUsuario2), ...;
```

### ENV

Para empezar a usar el bot hay que crear un archivo ".env" que tendrá los siguientes datos
```
TOKEN=(token de telegram)
DB_USER=(usuario del bot en la base de datos)
DB_PSSW=(contraseña del bot en la base de datos)
HOST=(direccion o nombre de red donde esté la base de datos)
DB=(Nombre de la base de datos)
```

### Ejecución

Una vez hecho todo lo anterior ejecutamos el programa main.py, esto hace que el bot ya esté funcional.

## Uso

Para añadir un nuevo puesto ejecutaremos el comando /new junto al nombre que le queramos dar al puesto.

Para pasar el turno y avisar a la siguiente persona usaremos el comando /next, en caso de que haya varios puestos que pasar usaremos /next junto al número de puestos que pasar.

Para los usuarios que vayan a reservar el bot les explicará como reservar.
