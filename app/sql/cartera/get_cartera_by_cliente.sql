SELECT 
    car.documento,
    CONVERT(date, CONVERT(varchar(8), car.fechafactura)) AS fechafactura,
    CONVERT(date, CONVERT(varchar(8), car.fechavencimiento)) AS fechavencimiento,

    DATEDIFF(
        day,
        CONVERT(date, CONVERT(varchar(8), car.fechavencimiento)),
        GETDATE()
    ) AS dias_vencido,

    car.saldo
FROM v_cartera_celuweb AS car
WHERE car.cliente = ?