from django.shortcuts import render


def scenario(request):
    id = request.GET.get("id")
    # get scenario texts according to ID
    infos = {
        "1": {
            "name": "Wind-Repowering",
            "kpi": {
                "total_production": [234, 8.3],
                "landuse": [8.8, 150],
                "wind": [100, 200],
                "pv": [111, 200],
                "biomass": [3, 50],
                "h2": [4.8, 125],
            },
            "description": [
                "Dieses Szenario setzt auf eine ausgewogene Mischung aus erneuerbaren Energiequellen, um die Klimaziele 2040 zu erreichen. Durch die Kombination von Photovoltaikanlagen, Windparks, Biomasse und Bioenergie wird der Energiebedarf nachhaltig gedeckt und die Abhängigkeit von einer einzelnen Energieart reduziert.",
                "Der Einsatz von PV-Anlagen auf Dächern und Freiflächen ergänzt die Windenergie und nutzt vorhandene Ressourcen optimal. Moderater Flächenverbrauch schützt natürliche Gebiete und berücksichtigt den Naturschutz.",
                "Einwohner und lokale Wirtschaft sind eingeladen, aktiv teilzunehmen. Die Maßnahmen sind nicht nur umweltschonend, sondern auch neu wirtschaftlich.",
            ],
            "pro": [
                "Ausgewogener Energiemix erhöht Resilienz und Zuverlässigkeit.",
                "Nutzung mehrerer erneuerbarer Quellen reduziert die Abhängigkeit von einer einzigen Energieart.",
                "Moderater Flächenverbrauch, wodurch natürliche Gebiete besser erhalten bleiben.",
            ],
            "contra": [
                "Komplexere Infrastruktur und Verwaltung aufgrund der Vielfalt der Energiequellen.",
                "Höhere Anfangskosten und logistische Herausforderungen beim Aufbau diverser erneuerbarer Projekte.",
            ],
        },
        "2": {
            "name": "Zubau Wind und PV",
            "kpi": {
                "total_production": [300, 25],
                "landuse": [12, 180],
                "wind": [180, 220],
                "pv": [120, 210],
                "biomass": [2.5, 30],
                "h2": [6, 140],
            },
            "description": {
                "In diesem Szenario wird der Ausbau von Windkraftanlagen und Photovoltaikanlagen stark vorangetrieben, um den wachsenden Energiebedarf zu decken und die Klimaziele 2040 zu erreichen.",
                "Durch den großflächigen Einsatz von Freiflächen-Photovoltaik und neuen Windparks steigt die Energieproduktion erheblich. Der Fokus liegt dabei auf der optimalen Nutzung vorhandener Flächen.",
                "Die lokale Bevölkerung wird in die Entscheidungsprozesse eingebunden, um die Akzeptanz der Maßnahmen zu erhöhen.",
            },
            "pro": [
                "Hohe Energieerträge durch den starken Ausbau von Wind- und PV-Anlagen.",
                "Geringere Abhängigkeit von fossilen Energieträgern durch die verstärkte Nutzung erneuerbarer Energien.",
                "Neue Arbeitsplätze in der erneuerbaren Energiebranche.",
            ],
            "contra": [
                "Hoher Flächenverbrauch für Photovoltaikanlagen könnte zu Konflikten mit Naturschutzbelangen führen.",
                "Erhöhte Investitionskosten aufgrund der umfangreichen Infrastrukturmaßnahmen.",
            ],
        },
        "3": {
            "name": "Zubau PV",
            "kpi": {
                "total_production": [220, 15],
                "landuse": [14, 200],
                "wind": [80, 150],
                "pv": [140, 250],
                "biomass": [1.8, 10],
                "h2": [2, 80],
            },
            "description": [
                "In diesem Szenario liegt der Schwerpunkt auf einem massiven Ausbau von Photovoltaikanlagen auf Dächern und Freiflächen. Ziel ist es, die Energieproduktion durch PV deutlich zu steigern.",
                "Durch den starken Zubau von PV-Anlagen wird ein großer Teil des Energiebedarfs gedeckt, insbesondere in sonnenreichen Regionen. Die Flächennutzung steigt entsprechend, was jedoch mit geringen Eingriffen in natürliche Gebiete kombiniert wird.",
                "Die lokale Bevölkerung profitiert von Einsparungen bei den Energiekosten, da die Nutzung von Solarenergie lokal verfügbar ist.",
            ],
            "pro": [
                "Deutliche Steigerung der Energieproduktion durch Photovoltaik.",
                "Geringe Betriebskosten nach der Installation.",
                "Wenig Emissionen bei der Energieproduktion.",
            ],
            "contra": [
                "Hoher Flächenverbrauch für PV-Anlagen auf Freiflächen.",
                "Saisonale Schwankungen bei der Energieproduktion, abhängig von Sonneneinstrahlung.",
            ],
        },
        "4": {
            "name": "Moorbewirtschaftung",
            "kpi": {
                "total_production": [150, 5],
                "landuse": [6, 50],
                "wind": [60, 100],
                "pv": [70, 120],
                "biomass": [20, 200],
                "h2": [0.5, 10],
            },
            "description": [
                "Dieses Szenario konzentriert sich auf die nachhaltige Bewirtschaftung von Mooren, um CO2-Emissionen zu verringern und die Biodiversität zu fördern.",
                "Durch die Renaturierung und nachhaltige Nutzung von Moorflächen kann nicht nur CO2 gebunden werden, sondern auch Energie aus Biomasse gewonnen werden. Die Energieproduktion steigt moderat, aber der Umweltnutzen ist signifikant.",
                "Die Maßnahmen zur Moorbewirtschaftung werden mit erneuerbaren Energiequellen wie Windkraft und Photovoltaik kombiniert, um die Energieproduktion zu ergänzen.",
            ],
            "pro": [
                "Erheblicher Beitrag zum Klimaschutz durch CO2-Bindung.",
                "Förderung der Biodiversität durch Renaturierung von Mooren.",
                "Zusätzliche Energiegewinnung aus Biomasse.",
            ],
            "contra": [
                "Geringere Gesamtenergieproduktion im Vergleich zu anderen Szenarien.",
                "Hohe Investitionskosten für Renaturierungsmaßnahmen.",
            ],
        },
        "5": {
            "name": "Wasserstoff",
            "kpi": {
                "total_production": [180, 10],
                "landuse": [7, 70],
                "wind": [100, 150],
                "pv": [60, 100],
                "biomass": [15, 80],
                "h2": [30, 300],
            },
            "description": [
                "In diesem Szenario wird der Fokus auf die Erzeugung und Nutzung von grünem Wasserstoff gelegt. Dieser wird als zentraler Energieträger für Industrie und Verkehr eingesetzt.",
                "Die Produktion von Wasserstoff erfolgt durch Elektrolyse, die durch erneuerbare Energien betrieben wird. Dies reduziert die Abhängigkeit von fossilen Brennstoffen und ermöglicht eine emissionsfreie Energieversorgung in verschiedenen Sektoren.",
                "Wasserstoff kann als Speichermedium genutzt werden, um Energieüberschüsse aus Wind- und Sonnenenergie auszugleichen.",
            ],
            "pro": [
                "Hohe Flexibilität bei der Nutzung von Wasserstoff als Energieträger.",
                "Speicherung und Nutzung von Energieüberschüssen.",
                "Reduzierung der CO2-Emissionen in der Industrie und im Verkehr.",
            ],
            "contra": [
                "Hohe Kosten für die Infrastruktur zur Wasserstofferzeugung und -verteilung.",
                "Geringe Effizienz bei der Umwandlung von Strom in Wasserstoff und zurück.",
            ],
        },
        "6": {
            "name": "Kostenoptimierung",
            "kpi": {
                "total_production": [210, 12],
                "landuse": [9, 100],
                "wind": [110, 170],
                "pv": [90, 180],
                "biomass": [7.5, 40],
                "h2": [5, 90],
            },
            "description": [
                "Das Szenario der Kostenoptimierung konzentriert sich darauf, die Energiewende kosteneffizient zu gestalten, ohne die langfristigen Klimaziele zu gefährden.",
                "Durch den Einsatz der kostengünstigsten Technologien und die Optimierung bestehender Infrastruktur wird die Energieproduktion gesteigert, während die Kosten im Vergleich zu anderen Szenarien geringer ausfallen.",
                "Die Nutzung von Wind- und Solarenergie wird gezielt ausgebaut, wobei der Fokus auf niedrigeren Investitions- und Betriebskosten liegt.",
            ],
            "pro": [
                "Geringere Investitionskosten im Vergleich zu anderen Szenarien.",
                "Effiziente Nutzung bestehender Infrastruktur und Technologien.",
                "Kosteneinsparungen für Verbraucher durch niedrigere Energiekosten.",
            ],
            "contra": [
                "Möglicherweise geringere Innovationskraft bei der Einführung neuer Technologien.",
                "Längere Amortisationszeiten bei bestimmten Investitionen.",
            ],
        },
        "7": {
            "name": "Hohe CO2-Preise",
            "kpi": {
                "total_production": [250, 18],
                "landuse": [10, 120],
                "wind": [120, 180],
                "pv": [100, 190],
                "biomass": [5, 70],
                "h2": [7, 150],
            },
            "description": [
                "Dieses Szenario basiert auf einem hohen CO2-Preis, der als wirtschaftlicher Anreiz dient, den Ausbau erneuerbarer Energien voranzutreiben und fossile Energieträger zu reduzieren.",
                "Durch hohe CO2-Kosten wird die Nutzung von Wind- und Solarenergie erheblich attraktiver, während die Nutzung von Kohle und Gas deutlich abnimmt. Unternehmen und Privatpersonen sind gezwungen, in klimafreundliche Technologien zu investieren.",
                "Die Energieproduktion wird durch verstärkte Nutzung erneuerbarer Energien gesteigert, während gleichzeitig der CO2-Ausstoß drastisch gesenkt wird.",
            ],
            "pro": [
                "Starker Anreiz zur Reduktion von CO2-Emissionen.",
                "Förderung von Investitionen in erneuerbare Energien.",
                "Langfristig wirtschaftliche Vorteile durch verringerte Abhängigkeit von fossilen Brennstoffen.",
            ],
            "contra": [
                "Erhebliche Kostensteigerungen für Verbraucher und Unternehmen durch hohe CO2-Preise.",
                "Mögliche soziale Ungleichheiten durch ungleiche Belastung.",
            ],
        },
        "8": {
            "name": "Suffizienz",
            "kpi": {
                "total_production": [180, 10],
                "landuse": [5, 50],
                "wind": [90, 130],
                "pv": [70, 100],
                "biomass": [10, 60],
                "h2": [2, 30],
            },
            "description": [
                "Das Szenario der Suffizienz zielt darauf ab, den Energieverbrauch durch Verhaltensänderungen und Effizienzsteigerungen zu reduzieren. Es setzt weniger auf den Ausbau erneuerbarer Energien und mehr auf den bewussten Umgang mit Ressourcen.",
                "Durch sparsamen Energieeinsatz und Reduktion des Konsums wird der Bedarf an neuer Energieinfrastruktur verringert. Die gesellschaftliche Akzeptanz für Einsparungen und bewussten Konsum ist dabei von zentraler Bedeutung.",
                "Energieeinsparungen werden durch Maßnahmen wie Energiesparprogramme, smarte Technologien und Förderung von Konsumverzicht erzielt.",
            ],
            "pro": [
                "Reduzierter Energieverbrauch und geringerer Bedarf an neuer Infrastruktur.",
                "Stärkung des Umweltbewusstseins und nachhaltiger Lebensstile.",
                "Weniger Eingriffe in natürliche Flächen durch geringere Energieproduktion.",
            ],
            "contra": [
                "Möglicherweise geringere Energieproduktion im Vergleich zu Szenarien mit starkem Ausbau erneuerbarer Energien.",
                "Hohe Abhängigkeit von Verhaltensänderungen der Bevölkerung, die schwer umsetzbar sind.",
            ],
        },
    }
    return render(request, "reenact/scenario.html", {"info": infos[id]})
