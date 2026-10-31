# DAX Measures

> Sesuaikan nama measure dasar dengan yang ada di model Anda. Tempel measure dasar Anda di bagian pertama.

## Measure dasar
```DAX
Revenue = -- tempel rumus Anda
Total Orders = -- tempel rumus Anda
Total Items Sold = -- tempel rumus Anda
Average Order Value = -- tempel rumus Anda
Total Discount = -- tempel rumus Anda
Total Customers = -- tempel rumus Anda
Total Shipping Fee = -- tempel rumus Anda
```

## Time intelligence
```DAX
Revenue LY = CALCULATE([Revenue], SAMEPERIODLASTYEAR(dim_date[date]))
Revenue YoY % = DIVIDE([Revenue] - [Revenue LY], [Revenue LY])
Revenue MoM % =
VAR prev = CALCULATE([Revenue], DATEADD(dim_date[date], -1, MONTH))
RETURN DIVIDE([Revenue] - prev, prev)

Orders YoY % =
VAR ly = CALCULATE([Total Orders], SAMEPERIODLASTYEAR(dim_date[date]))
RETURN DIVIDE([Total Orders] - ly, ly)

Items Sold YoY % =
VAR ly = CALCULATE([Total Items Sold], SAMEPERIODLASTYEAR(dim_date[date]))
RETURN DIVIDE([Total Items Sold] - ly, ly)

AOV YoY % =
VAR ly = CALCULATE([Average Order Value], SAMEPERIODLASTYEAR(dim_date[date]))
RETURN DIVIDE([Average Order Value] - ly, ly)

Customers YoY % =
VAR ly = CALCULATE([Total Customers], SAMEPERIODLASTYEAR(dim_date[date]))
RETURN DIVIDE([Total Customers] - ly, ly)
```

## Diskon dan pengiriman
```DAX
Discount % = DIVIDE([Total Discount], [Revenue] + [Total Discount])
Avg Delivery Days = AVERAGE(fact_pengiriman[delivery_days])
Delivered Rate =
DIVIDE(
    CALCULATE(COUNTROWS(fact_pengiriman), fact_pengiriman[tracking_status] = "Terkirim"),
    COUNTROWS(fact_pengiriman)
)
Pengiriman Tertunda =
CALCULATE(COUNTROWS(fact_pengiriman), fact_pengiriman[tracking_status] = "Belum Dikirim")
```

## Kolom kalkulasi dim_date
```DAX
Year = YEAR(dim_date[date])
Month Number = MONTH(dim_date[date])
Month Name = FORMAT(dim_date[date], "MMMM")
Month Short = FORMAT(dim_date[date], "MMM")
Quarter = "Q" & ROUNDUP(MONTH(dim_date[date]) / 3, 0)
Year Month = FORMAT(dim_date[date], "YYYY-MM")
```
