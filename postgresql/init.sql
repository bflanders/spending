
drop table if exists spending;

drop table if exists spending_categories;

create table if not exists spending_categories (type text primary key);

insert into spending_categories
    values ('Gas'),('Clothes'),('Extra'),('Food'),('Take Out');

create table spending (
    id serial
    ,date date not null
    ,store text not null
    ,amount double precision
    ,category text references spending_categories(type)
    ,comment text
);

create index spending_types_idx on spending(category);
