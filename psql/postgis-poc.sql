```
drop table college;

create table college(
    name varchar(100),
    geo geography(Point,4326)
);


INSERT INTO college (name, geo) VALUES
    ( 'L.D', 'POINT(23.032410 72.547960)'),
    ( 'CEPT', 'POINT(23.035890 72.548390)'),
    ( 'GP', 'POINT(23.025480 72.549110)'),
    ( 'R.C. Technical', 'POINT(23.078430 72.535830)'),
    ('Marine Drive', 'POINT(18.944941 72.825699)'),
    ('Gateway Of India', 'POINT(18.921966 72.834566)');

SELECT name, ST_Distance(
    ST_Transform(geo::geometry,900913),
    ST_Transform(ST_GeomFromText('POINT(23.078430 72.535830)', 4326),900913)
) from college;


select name, ST_Distance_Spheroid(geo::geography, ST_GeomFromText('POINT(23.032410 72.547960)',4326), 'SPHEROID["WGS 84",6378137,298.257223563]') from college;
```
