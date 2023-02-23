# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import timedelta
import pytz
import pathlib
import os
import logging
import base64
_logger = logging.getLogger(__name__)

from fitz import fitz, Rect

def add_signature(pdf, img_file, w, h, x1, x2, site="right", skip_pages = 1):
    
    '''
    The higher w , the more left-sided the image will be positioned 
    The higher h, the less the distance to the bottom of the page
    The higher x1, the more left-sided the image will be positioned 
    The lower x2, the higher the image will be positioned and the bigger the image will get
    
    If you want to have the image on the left hand side, pass "left" as an argument to site.
    By default it will be set to "right".
    
    If you want to skip some of the last pages, pass the number of pages to "skip_pages". 
    By default the last page will be skipped. If you want to skip the last two pages, pass 2 to skip_pages and so on
    '''
    
    # Define which image should be inserted
    img = open(img_file, "rb").read()
    
    if site == "right":
        rect = fitz.Rect(w * x1, h * x2, w, h)
    else:
        rect = fitz.Rect(w * x1 * -1 * 0.94, h * x2, w, h)

    rect = fitz.Rect(70, 650, 170, 710)#x0, y0, x1, y1
    # Rect represents a rectangle defined by four floating point numbers x0, y0, x1, y1. 
    # They are treated as being coordinates of two diagonally opposite points. 
    # The first two numbers are regarded as the “top left” corner P(x0,y0) and P(x1,y1) as the “bottom right” one. 
    # However, these two properties need not coincide with their intuitive meanings – read on.
    print("rect ===>>>", rect)

    for i in range(0, pdf.page_count):
        if i == 1:
        # if i < pdf.page_count - skip_pages:
            page = pdf[i]
            if not page.is_wrapped:
                page.wrap_contents()
            page.insert_image(rect, stream=img)

def add_date_signed(pdf, rect_x1, rect_y1, rect_x2, rect_y2, text):
    fontsize_to_use = 12
    # text = "12/02/2023"
    fontname_to_use = "Times-Roman"
    text_lenght = fitz.get_text_length(text, 
                                    fontname=fontname_to_use, 
                                    fontsize=fontsize_to_use)

    # rect = (170, 700, 280, 750)
    rect = (rect_x1, rect_y1, rect_x2, rect_y2)
    print("rect ===>>>", rect)

    for i in range(0, pdf.page_count):
        if i == 1:
            page = pdf[i]
            rc = page.insert_textbox(rect, text,
                                    fontsize=fontsize_to_use,
                                    fontname=fontname_to_use,
                                    align=1)


def add_customer_name(pdf, rect_x1, rect_y1, rect_x2, rect_y2, text):
    fontsize_to_use = 12
    fontname_to_use = "Times-Roman"
    text_lenght = fitz.get_text_length(text, 
                                    fontname=fontname_to_use, 
                                    fontsize=fontsize_to_use)

    # rect = (170, 700, 280, 750)
    rect = (rect_x1, rect_y1, rect_x2, rect_y2)
    print("rect ===>>>", rect)

    for i in range(0, pdf.page_count):
        if i == 1:
            page = pdf[i]
            rc = page.insert_textbox(rect, text,
                                    fontsize=fontsize_to_use,
                                    fontname=fontname_to_use,
                                    align=1)





class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection(
       string='Order Type',
       selection=[('delivery_tent', 'Delivery & Tent Setup'),
                  ('client_pickup', 'Client Pickup'),
                  ('ground_delivery', 'Ground Delivery'),
                  ('ground_delivery_pickup', 'Ground Delivery & Pickup'),
        ], default='delivery_tent')
    event_start = fields.Datetime(
        string='Event Start',
        default=fields.Datetime.now,
        store=True,
    )
    event_end = fields.Datetime(
        string='Event End',
        default=lambda self: fields.Datetime.now() + timedelta(hours=1),
        store=True,
    )
    order_note = fields.Char()
    
    agreement_signed = fields.Boolean()
    


    def utc_to_local(self, utc):
        if self.env.user.id == 1:
            user_tz = self.env['res.users'].search([])[0].tz
        else:
            user_tz = self.env.user.tz or pytz.utc 
        print('user_tz ===>>>', user_tz)
        local = pytz.timezone(user_tz)
        return utc.astimezone(local)

    def convert_utc_to_local(self, utc):
        local = self.utc_to_local(utc)
        local = local - timedelta(hours=13)
        local = local.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        print('utc ===>>>', utc)
        print('local ===>>>', local)
        return local
    
    def add_contract_sign(self, attachment_id, signed_by, signed_on, signature):
        module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        folder_path = module_path + "/store/"
        print('folder_path ===>>>', folder_path)

        file_name = folder_path + self.name + "-" + attachment_id.name
        convert_file_name = folder_path + self.name + "_" + attachment_id.name.replace(".pdf","") + "_signed.pdf"
        
        with open(file_name, 'wb') as pdf_file:
            pdf_file.write(base64.b64decode(attachment_id.datas))


        doc = fitz.open(file_name)

        # location parameters
        w = 570
        h = 400
        x1 = 0.945
        x2 = 0.96


        img_file_name = folder_path + self.partner_id.name +  "_signature.png"
        with open(img_file_name, 'wb') as img_file:
            img_file.write(base64.b64decode(signature))


        add_signature(doc, img_file_name, w, h, x1, x2, "left")
        rect_x1, rect_y1, rect_x2, rect_y2 = 170, 700, 280, 750
        date_signed = signed_on.strftime("%d/%m/%Y")
        print('date_signed ===>>>', date_signed)
        add_date_signed(doc, rect_x1, rect_y1, rect_x2, rect_y2, date_signed)

        rect_x1, rect_y1, rect_x2, rect_y2 = 290, 700, 400, 750
        signed_by = signed_by[0:16]
        print('signed_by ===>>>', signed_by)
        add_customer_name(doc, rect_x1, rect_y1, rect_x2, rect_y2, signed_by)
        doc.save(convert_file_name)  

        #Update ir.attachment
        ####################################################################
        with open(convert_file_name, 'rb') as convert_file_pdf:
            data = base64.b64encode(convert_file_pdf.read())
            attachment_id.datas = data
            self.agreement_signed = True
        #####################################################################

        #Remove all the files
        os.remove(file_name)
        os.remove(convert_file_name)
        os.remove(img_file_name)
    

   
    
    

