CREATE TABLE tb_book(
   id             INT PRIMARY KEY     NOT NULL,
   name           CHAR(16)    NOT NULL,
   author         CHAR(16)     NOT NULL,
   intro          TEXT
);


CREATE TABLE tb_catalog(
   id             INT PRIMARY KEY     NOT NULL,
   book_id        INT    NOT NULL,
   chapter_id     INT    NOT NULL,
   title          CHAR(16)     NOT NULL,
   intro          TEXT
);

CREATE TABLE tb_article(
   id             INT PRIMARY KEY     NOT NULL,
   author         CHAR(16),
   `date`         CHAR(16),
   content        TEXT,
   footnotes          TEXT
);