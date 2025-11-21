SELECT 
    car.cliente as nit,
    SUM(car.saldo) AS total_saldo,
    SUM(
        CASE 
            WHEN DATEDIFF(
                    day,
                    CONVERT(date, CONVERT(varchar(8), car.fechavencimiento)),
                    GETDATE()
                 ) > 0 
            THEN car.saldo 
            ELSE 0 
        END
    ) AS total_vencido

FROM v_cartera_celuweb AS car
GROUP BY car.cliente;