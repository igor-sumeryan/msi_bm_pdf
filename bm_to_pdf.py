import io
from playwright.async_api import async_playwright
import img2pdf
import PyPDF2
from PIL import Image

class pdfConverter:

    def __init__(self, url: str, measurement: str):
        self.url = url
        self.measurement = measurement

    async def create_pdf(self) -> bytes:

        # Screenshot da capa
        url_cover = f"https://arteris.meb.services/capa_boletim?id={self.measurement}"
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url_cover)
            await page.wait_for_load_state('networkidle')
            # Salva a página em PDF
            bytes_cover_image = await page.screenshot(full_page=True)
            await browser.close()
        
        # Screenshot do boletim
        url_measurement = f"https://arteris.meb.services/boletim_medicao_fixo?id={self.measurement}"
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url_measurement)
            await page.wait_for_load_state('networkidle')
            # Salva a página em PDF
            bytes_measurement_image = await page.screenshot(full_page=True)
            await browser.close()

        pdf_cover = img2pdf.convert(bytes_cover_image)
        pdf_measurement = img2pdf.convert(bytes_measurement_image)

        pdfMerge = PyPDF2.PdfMerger()
        pdfMerge.append(pdf_cover)
        pdfMerge.append(pdf_measurement)

        output_buffer = io.BytesIO()
        pdfMerge.write(output_buffer)

        merged_pdf_bytes = output_buffer.getvalue()

        pdfMerge.close()

        # Implement the PDF conversion logic here
        return merged_pdf_bytes

