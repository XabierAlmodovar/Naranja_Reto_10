document.addEventListener('DOMContentLoaded', () => {

    /* ===============================
       GRÁFICO 1 — PIE CHART CONVERSIÓN
    =============================== */
    const completionData = [
        { label: 'Completan', value: 32 },
        { label: 'Abandonan', value: 9 }
    ];
    drawPieChart('#completionChart', completionData, 'Conversión del Onboarding');

    /* ===============================
       GRÁFICO 2 — TIEMPO POR SECCIÓN
    =============================== */
    const timeBySectionData = [
        { label: 'Ojos', value: 7 },
        { label: 'Pelo', value: 8 },
        { label: 'Leisure', value: 12 },
        { label: 'Estilo', value: 52 },
        { label: 'Fotos', value: 61 },
        { label: 'Tallas', value: 29 },
        { label: 'Sign-Up', value: 28 }
    ];
    drawHorizontalBarChart('#timeBySectionChart', timeBySectionData, 'Tiempo Mediano por Sección (s)');

    /* ===============================
       GRÁFICO 3 — BLOQUEO EN FOTOS
    =============================== */
    const photosBlockingData = [
        { label: 'Avanzan', value: 61 },
        { label: 'Retroceden', value: 460 }
    ];
    drawBarChart('#photosBlockingChart', photosBlockingData, 'Bloqueo Crítico en Fotos');

    /* ===============================
       GRÁFICO 4 — FLUJO DE USUARIO (AVANCE VS RETROCESO)
    =============================== */
    const flowData = [
        { section: 'Ojos', advance: 32, back: 0 },
        { section: 'Pelo', advance: 32, back: 1 },
        { section: 'Leisure', advance: 18, back: 14 },
        { section: 'Estilo', advance: 25, back: 7 },
        { section: 'Fotos', advance: 61, back: 460 },
        { section: 'Tallas', advance: 28, back: 12 },
        { section: 'Sign-Up', advance: 32, back: 0 }
    ];
    drawStackedBarChart('#flowChart', flowData, 'Flujo de Usuario: Avance vs Retroceso');
});

/* ===============================
   FUNCIONES D3
=============================== */

/* ---- PIE CHART ---- */
function drawPieChart(container, data, title) {
    const width = 400;
    const height = 400;
    const radius = Math.min(width, height) / 2 - 40;

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2}, ${height / 2})`);

    svg.append('text')
        .attr('y', -radius - 20)
        .attr('text-anchor', 'middle')
        .text(title)
        .style('font-size', '16px')
        .style('font-weight', 'bold'); // YA ESTABA, SE MANTIENE

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.label))
        .range(["#EEC7C0", "#6BA6A9"]);

    const pie = d3.pie()
        .value(d => d.value)
        .sort(null);

    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    const arcs = svg.selectAll('arc')
        .data(pie(data))
        .enter()
        .append('g')
        .attr('class', 'arc');

    arcs.append('path')
        .attr('d', arc)
        .attr('fill', d => color(d.data.label));

    arcs.append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('text-anchor', 'middle')
        .attr('dy', '0.35em')
        .text(d => `${d.data.label}: ${d.data.value}`)
        .style('fill', '#fff')
        .style('font-size', '12px');
}

/* ---- BARRA VERTICAL SIMPLE ---- */
function drawBarChart(container, data, title) {
    const width = 500;
    const height = 300;
    const margin = { top: 40, right: 20, bottom: 40, left: 40 };

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // CORREGIDO: AÑADIDA NEGRITA Y TAMAÑO
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', 20)
        .attr('text-anchor', 'middle')
        .text(title)
        .style('font-size', '16px')   // Añadido para igualar a los otros
        .style('font-weight', 'bold'); // Añadido para negrita

    const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([margin.left, width - margin.right])
        .padding(0.3);

    const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
        .range([height - margin.bottom, margin.top]);

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => x(d.label))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => y(0) - y(d.value))
        .attr('fill', "#9ECBCF");
}

/* ---- BARRA HORIZONTAL ---- */
function drawHorizontalBarChart(container, data, title) {
    const width = 600;
    const height = 350;
    const margin = { top: 40, right: 20, bottom: 40, left: 100 };

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // CORREGIDO: AÑADIDA NEGRITA Y TAMAÑO
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', 20)
        .attr('text-anchor', 'middle')
        .text(title)
        .style('font-size', '16px')   // Añadido para igualar a los otros
        .style('font-weight', 'bold'); // Añadido para negrita

    const y = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([margin.top, height - margin.bottom])
        .padding(0.3);

    const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .nice()
        .range([margin.left, width - margin.right]);

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('y', d => y(d.label))
        .attr('x', x(0))
        .attr('height', y.bandwidth())
        .attr('width', d => x(d.value) - x(0))
        .attr('fill', "#EEC7C0");
}

/* ---- BARRA APILADA (AVANCE VS RETROCESO) ---- */
function drawStackedBarChart(container, data, title) {
    const width = 700;
    const height = 400;
    const margin = { top: 50, right: 20, bottom: 50, left: 100 };

    const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    svg.append('text')
        .attr('x', width / 2)
        .attr('y', 25)
        .attr('text-anchor', 'middle')
        .text(title)
        .style('font-size', '16px')
        .style('font-weight', 'bold'); // YA ESTABA, SE MANTIENE

    const y = d3.scaleBand()
        .domain(data.map(d => d.section))
        .range([margin.top, height - margin.bottom])
        .padding(0.3);

    const x = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.advance + d.back)])
        .nice()
        .range([margin.left, width - margin.right]);

    const color = d3.scaleOrdinal()
        .domain(['advance', 'back'])
        .range(["#EEC7C0", "#6BA6A9"]);

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('g')
        .each(function(d) {
            d3.select(this)
                .append('rect')
                .attr('y', y(d.section))
                .attr('x', x(0))
                .attr('height', y.bandwidth())
                .attr('width', x(d.advance) - x(0))
                .attr('fill', color('advance'));

            d3.select(this)
                .append('rect')
                .attr('y', y(d.section))
                .attr('x', x(d.advance))
                .attr('height', y.bandwidth())
                .attr('width', x(d.back) - x(0))
                .attr('fill', color('back'));
        });

    // Leyenda
    const legend = svg.append('g')
        .attr('transform', `translate(${width - margin.right - 120}, ${margin.top})`);

    legend.selectAll('rect')
        .data(['Avanzan', 'Retroceden'])
        .enter()
        .append('rect')
        .attr('x', 0)
        .attr('y', (d,i) => i * 25)
        .attr('width', 20)
        .attr('height', 20)
        .attr('fill', d => d === 'Avanzan' ? "#EEC7C0" : "#6BA6A9"); 

    legend.selectAll('text')
        .data(['Avanzan', 'Retroceden'])
        .enter()
        .append('text')
        .attr('x', 30)
        .attr('y', (d,i) => i * 25 + 15)
        .text(d => d)
        .style('font-size', '12px');
}