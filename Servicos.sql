DECLARE @DataRef AS DATE = '{dataParam}';

SELECT DISTINCT 
    TblS.Empresa,
    TblS.DataViagem AS 'Data',
    TblL.NomeLinha AS 'Linha',
    TblL.NroLinha AS 'Número da Linha',
    TblS.NroServico AS 'Serviço',
    TblS.HoraViagem AS 'Horário',
	TblS.ASK AS 'ASK',

	sum(TblB.Distancia) AS 'RPK',
    
    CAST(
        SUM(CASE 
                WHEN TblB.IdTipoPassagem <> 4 
                     AND TblB.IdStatus IN (1, 7, 8) 
                THEN TblB.Distancia 
                ELSE 0 
            END) / TblS.ASK 
        AS NUMERIC(10, 4)
    ) AS 'IAP%',

    FORMAT(
        ISNULL(
            SUM(CASE 
                    WHEN TblB.IdTipoPassagem <> 4 
                         AND TblB.IdStatus IN (1, 7, 8) 
                    THEN TblB.Total 
                END) / (
                    SELECT MAX(KmRodado)
                    FROM TblServico sv1
                    WHERE TblS.IdLinha = sv1.IdLinha
					AND TBLS.DataViagem = sv1.DataViagem
                ),
            0
        ),
        'N', 
        'pt-BR'
    ) AS 'R$/KM'

FROM 
    dbo.TblServico AS TblS
    INNER JOIN dbo.TblLinha AS TblL ON TblS.LinhaClasse = TblL.LinhaClasse AND TBLL.IDLINHA = TBLS.IdLinha
    LEFT JOIN dbo.TblBilhete AS TblB ON TblB.IdServico = TblS.IdServico

WHERE 
    TblS.Empresa IN ('VIACAO MOTTA', 'VIACAO TOTAL', 'PLANALTO')
    AND TblS.Status IN ('ABERTO', 'FECHADO')
    AND CONVERT(DATE, TblS.DataViagem) = @DataRef
    AND TblL.SubGrupo <> ''
    AND TblS.NroServico < '98000000'
	and TBLB.IdStatus IN (1,7,8)
	AND TBLB.IdTipoPassagem <> 4

GROUP BY 
    TblS.Empresa,
    TblS.DataViagem,
    TblL.NomeLinha,
    TblL.NroLinha,
    TblS.NroServico,
    TblS.HoraViagem,
    TblS.ASK,
    TblS.IdLinha;
