import asyncio
from playwright.async_api import async_playwright
import img2pdf
import PyPDF2
from PIL import Image



async def main():
    url = "https://arteris.meb.services/capa_boletim?id=BM-CW31091-001"
    pdf_filename = "capa_boletim_BM-CW31091-001.pdf"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False exibe o Chromium
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        # Salva a página em PDF
        await page.screenshot(path="capa.png", full_page=True)
        await page.pdf(path=pdf_filename, format="A4", prefer_css_page_size=True)
        print(f"PDF salvo como {pdf_filename}")
        await browser.close()

    # open each image
    with Image.open("capa.png") as image: 
        # convert the image to a PDF
        pdf = img2pdf.convert(image.filename)
        # write the PDF to its final destination
        with open(f"capa.pdf", "wb") as file:
            file.write(pdf)
        print(f"Converted capa.png to capa.pdf")

    url = "https://arteris.meb.services/boletim_medicao_fixo?uuid=019745f0-eb1e-7651-b4e9-a9e0e118a4aa"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # headless=False exibe o Chromium
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        # Captura a coluna rolavel scrollableColumns
        scrollableColumns = await page.query_selector_all('.scrollable-column')
        for column in scrollableColumns:
            await column.scroll_into_view_if_needed()

        # Salva a página em PDF
        await page.screenshot(path="boletim.png", full_page=True)
        await page.pdf(path=pdf_filename, format="A4", prefer_css_page_size=True)
        print(f"PDF salvo como {pdf_filename}")
        await browser.close()

    # open each image
    with Image.open("boletim.png") as image: 
        # convert the image to a PDF
        pdf = img2pdf.convert(image.filename)
        # write the PDF to its final destination
        with open(f"boletim.pdf", "wb") as file:
            file.write(pdf)
        print(f"Converted boletim.png to boletim.pdf")

    pdfMerge = PyPDF2.PdfMerger()
    # loop through each pdf page
    pdfs=["capa.pdf", "boletim.pdf"]
    for pdf in pdfs:
        # open each pdf
        with open(pdf, 'rb') as pdfFile:
            # merge each file
            pdfMerge.append(PyPDF2.PdfReader(pdfFile))    

    # write the merged pdf 
    pdfMerge.write('merged.pdf')
    pdfMerge.close()

if __name__ == "__main__":
    asyncio.run(main())
