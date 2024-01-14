create table main.user
(
    id          TEXT
        primary key,
    name        TEXT                  not null,
    email       TEXT                  not null
        unique,
    profile_pic TEXT                  not null,
    is_admin    boolean default false null on conflict replace
);




create table main.animals
(
    id          INTEGER not null
        primary key autoincrement ,
    name        TEXT    not null,
    user_id     TEXT
        references main.user,
    kind        TEXT    not null,
    breed       TEXT,
    sex         TEXT,
    age         TEXT,
    description TEXT,
    img_url     TEXT    not null,
    location    TEXT,
    adopted     boolean default 0
);


create table main.adoption_forms
(
    user_id             TEXT
        references main.user,
    animal_id           TEXT
        references main.animals,
    owner_id            TEXT
        references main.user,
    user_age            TEXT,
    location            TEXT,
    building_type       TEXT,
    current_pets        TEXT,
    previous_experience TEXT,
    phone_number        TEXT,
    status              TEXT default "pending",
    primary key (user_id, animal_id)
);

