create table question
(
    id              serial
        constraint pk_question_id
            primary key,
    submission_time timestamp default CURRENT_TIMESTAMP,
    view_number     integer,
    vote_number     integer   default 0,
    title           text,
    message         text,
    image           text      default ''::text
);

alter table question
    owner to postgres;

create table answer
(
    id              serial
        constraint pk_answer_id
            primary key,
    submission_time timestamp default CURRENT_TIMESTAMP,
    vote_number     integer   default 0,
    question_id     integer
        constraint fk_question_id
            references question,
    message         text,
    image           text      default ''::text
);

alter table answer
    owner to postgres;

create table comment
(
    id              serial
        constraint pk_comment_id
            primary key,
    question_id     integer
        constraint fk_question_id
            references question,
    answer_id       integer
        constraint fk_answer_id
            references answer,
    message         text,
    submission_time timestamp,
    edited_count    integer
);

alter table comment
    owner to postgres;

create table tag
(
    id   serial
        constraint pk_tag_id
            primary key,
    name text
);

alter table tag
    owner to postgres;

create table question_tag
(
    question_id integer not null
        constraint fk_question_id
            references question,
    tag_id      integer not null
        constraint fk_tag_id
            references tag,
    constraint pk_question_tag_id
        primary key (question_id, tag_id)
);

alter table question_tag
    owner to postgres;

