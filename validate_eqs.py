from docx.oxml import parse_xml

eqs = [
    '<m:sSub><m:e><m:r><m:t>T</m:t></m:r></m:e><m:sub><m:r><m:t>ciclo</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>60</m:t></m:r></m:num><m:den><m:r><m:t>C</m:t></m:r></m:den></m:f><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>60</m:t></m:r></m:num><m:den><m:r><m:t>120</m:t></m:r></m:den></m:f><m:r><m:t> = 0.500 s = 500 ms</m:t></m:r>',
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>tránsito</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>d</m:t></m:r></m:num><m:den><m:r><m:t>v</m:t></m:r></m:den></m:f><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>0.85 m</m:t></m:r></m:num><m:den><m:r><m:t>1.20 m/s</m:t></m:r></m:den></m:f><m:r><m:t> ≈ 0.708 s = 708 ms</m:t></m:r>',
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>respuesta</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>adq</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>prep</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>ocr</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>plc</m:t></m:r></m:sub></m:sSub><m:r><m:t> = 15 + 25 + 90 + 45 = 175 ms</m:t></m:r>',
    '<m:sSub><m:e><m:r><m:t>FS</m:t></m:r></m:e><m:sub><m:r><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r><m:f><m:num><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>tránsito</m:t></m:r></m:sub></m:sSub></m:num><m:den><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>respuesta</m:t></m:r></m:sub></m:sSub></m:num></m:f><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>708 ms</m:t></m:r></m:num><m:den><m:r><m:t>175 ms</m:t></m:r></m:den></m:f><m:r><m:t> ≈ 4.05 &gt; 4.0</m:t></m:r>',
    '<m:r><m:t>B = v · </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>exp</m:t></m:r></m:sub></m:sSub>',
    '<m:sSub><m:e><m:r><m:t>B</m:t></m:r></m:e><m:sub><m:r><m:t>conv</m:t></m:r></m:sub></m:sSub><m:r><m:t> = (1.20 m/s) · </m:t></m:r><m:d><m:e><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>30</m:t></m:r></m:den></m:f><m:r><m:t> s</m:t></m:r></m:e></m:d><m:r><m:t> = 0.040 m = 40.0 mm</m:t></m:r>',
    '<m:sSub><m:e><m:r><m:t>B</m:t></m:r></m:e><m:sub><m:r><m:t>estrobo</m:t></m:r></m:sub></m:sSub><m:r><m:t> = (1.20 m/s) · </m:t></m:r><m:d><m:e><m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2000</m:t></m:r></m:den></m:f><m:r><m:t> s</m:t></m:r></m:e></m:d><m:r><m:t> = (1.20 m/s) · (0.0005 s) = 0.0006 m = 0.60 mm</m:t></m:r>',
    '<m:r><m:t>Y = 0.299 · R + 0.587 · G + 0.114 · B</m:t></m:r>',
    '<m:sSubSup><m:e><m:r><m:t>σ</m:t></m:r></m:e><m:sub><m:r><m:t>B</m:t></m:r></m:sub><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSubSup><m:r><m:t>(k) = </m:t></m:r><m:f><m:num><m:sSup><m:e><m:d><m:e><m:sSub><m:e><m:r><m:t>μ</m:t></m:r></m:e><m:sub><m:r><m:t>T</m:t></m:r></m:sub></m:sSub><m:r><m:t> · ω(k) - μ(k)</m:t></m:r></m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:num><m:den><m:r><m:t>ω(k) · [1 - ω(k)]</m:t></m:r></m:den></m:f>',
    '<m:r><m:t>Payback = </m:t></m:r><m:f><m:num><m:r><m:t>CAPEX</m:t></m:r></m:num><m:den><m:r><m:t>Ahorro Mensual</m:t></m:r></m:den></m:f><m:r><m:t> = </m:t></m:r><m:f><m:num><m:r><m:t>$385 USD</m:t></m:r></m:num><m:den><m:r><m:t>$4,200 USD/mes</m:t></m:r></m:den></m:f><m:r><m:t> ≈ 0.091 meses ≈ 2.7 días</m:t></m:r>'
]

for i, eq in enumerate(eqs, 1):
    xml_str = f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{eq}</m:oMath>'
    node = parse_xml(xml_str)
    print(f"Eq {i} parsed successfully!")

print("All 10 equations are 100% valid OMML!")
