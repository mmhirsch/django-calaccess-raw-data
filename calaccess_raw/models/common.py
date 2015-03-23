from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from .base import CalAccessBaseModel


@python_2_unicode_compatible
class FilernameCd(CalAccessBaseModel):
    """
    A combination of CAL-ACCESS tables to provide the analyst with
    filer information.

    Note: Name last can also be the full name of the filer
    (for both Campaign and lobbying filing entities).

    Full name of all pacs, firms, and employers are always in this last
    name field.

    Major donors can be split between first and last name fields, but usually
    are contained in the last name field only. Individual names of lobbyists,
    candidates/officeholders, treasurers/responsible officers, and major donors
    (when they are only an individual's name) use both the first and last name
    fields in conjunction.
    """
    xref_filer_id = models.CharField(
        max_length=15,
        db_column='XREF_FILER_ID',
        db_index=True,
        help_text="The external filer id saved in the forms tables"
    )
    filer_id = models.IntegerField(
        db_column='FILER_ID',
        db_index=True,
        null=True,
        help_text="The internal filer id saved in Cal-Access"
    )
    filer_type = models.CharField(
        max_length=45,
        db_column='FILER_TYPE',
        db_index=True,
    )
    status = models.CharField(max_length=10, db_column='STATUS')
    effect_dt = models.DateField(
        db_column='EFFECT_DT',
        help_text="Effective date for status",
        null=True,
    )
    naml = models.CharField(
        max_length=200, db_column='NAML',
        help_text="Last name, (though sometimes the full name)"
    )
    namf = models.CharField(
        max_length=55, db_column='NAMF', blank=True,
        help_text="First name"
    )
    namt = models.CharField(
        max_length=70, db_column='NAMT', blank=True,
        help_text="Name prefix or title"
    )
    nams = models.CharField(
        max_length=32, db_column='NAMS', blank=True,
        help_text="Name suffix"
    )
    adr1 = models.CharField(max_length=200, db_column='ADR1', blank=True)
    adr2 = models.CharField(max_length=200, db_column='ADR2', blank=True)
    city = models.CharField(max_length=55, db_column='CITY', blank=True)
    st = models.CharField(max_length=4, db_column='ST', blank=True)
    zip4 = models.CharField(max_length=10, db_column='ZIP4', blank=True)
    phon = models.CharField(max_length=60, db_column='PHON', blank=True)
    fax = models.CharField(max_length=60, db_column='FAX', blank=True)
    email = models.CharField(max_length=60, db_column='EMAIL', blank=True)

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'FILERNAME_CD'
        verbose_name = 'FILERNAME_CD'
        verbose_name_plural = 'FILERNAME_CD'
        ordering = ("naml", "namf",)

    def __str__(self):
        return str(self.filer_id)


@python_2_unicode_compatible
class FilerFilingsCd(CalAccessBaseModel):
    """
    Key table that links filers to their paper, key data entry, legacy,
    and electronic filings. This table is used as an index to locate
    filing information.
    """
    filer_id = models.IntegerField(
        db_column='FILER_ID',
        db_index=True,
        help_text="Filer's unique identification number"
    )
    filing_id = models.IntegerField(
        db_column='FILING_ID',
        db_index=True,
        verbose_name='filing ID',
        help_text="Unique filing identificiation number"
    )
    period_id = models.IntegerField(
        null=True,
        db_column='PERIOD_ID',
        blank=True,
        help_text="Identifies the period when the filing was recieved."
    )
    form_id = models.CharField(max_length=7, db_column='FORM_ID')
    filing_sequence = models.IntegerField(
        db_column='FILING_SEQUENCE',
        db_index=True,
        help_text="Amendment number where 0 is an original filing and 1 to \
999 are amendments"
    )
    filing_date = models.DateField(
        db_column='FILING_DATE',
        help_text="Date the filing was entered into the system",
        null=True
    )
    stmnt_type = models.IntegerField(
        db_column='STMNT_TYPE',
        help_text="Type of statement. (Logged paper, electronic or KDE \
filing"
    )
    stmnt_status = models.IntegerField(
        db_column='STMNT_STATUS',
        null=True,
        help_text="The status of the statement. If the filing has been \
reviewed or not reviewed."
    )
    session_id = models.IntegerField(
        db_column='SESSION_ID',
        help_text="Legislative session that the filing applies to"
    )
    user_id = models.CharField(max_length=12, db_column='USER_ID')
    special_audit = models.IntegerField(
        null=True,
        db_column='SPECIAL_AUDIT',
        blank=True,
        help_text="Denotes whether the filing has been audited for money \
laundering or other special condition."
    )
    fine_audit = models.IntegerField(
        null=True,
        db_column='FINE_AUDIT',
        blank=True,
        help_text="Indicates whether a filing has been audited for a fine"
    )
    rpt_start = models.DateField(
        null=True,
        db_column='RPT_START',
        blank=True,
        help_text="Starting date for the period the filing represents",
    )
    rpt_end = models.DateField(
        null=True,
        db_column='RPT_END',
        blank=True,
        help_text="Ending date for the period the filing represents",
    )
    rpt_date = models.DateField(
        null=True,
        db_column='RPT_DATE',
        blank=True,
        help_text="When SOS recieved the filing",
    )
    FILING_TYPE_CHOICES = (
        (None, 'None'),
        ('22000', 'Filing type'),
        ('22001', 'Electronic'),
        ('22002', 'Key data entry'),
        ('22003', 'Historical lobby'),
        ('22004', 'Historical campaign'),
        ('22005', 'AMS'),
        ('22006', 'Cal Online'),
    )
    filing_type = models.IntegerField(
        db_column='FILING_TYPE',
        null=True,
        blank=True,
        choices=FILING_TYPE_CHOICES
    )

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'FILER_FILINGS_CD'
        verbose_name = 'FILER_FILINGS_CD'
        verbose_name_plural = 'FILER_FILINGS_CD'

    def __str__(self):
        return str("%s %s" % (self.filer_id, self.filing_id))


@python_2_unicode_compatible
class FilingsCd(CalAccessBaseModel):
    """
    This table is the parent table from which all links and association to
    a filing are derived.
    """
    filing_id = models.IntegerField(
        db_column='FILING_ID',
        db_index=True,
        verbose_name='filing ID',
        help_text="Unique filing identificiation number"
    )
    filing_type = models.IntegerField(db_column='FILING_TYPE')

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'FILINGS_CD'
        verbose_name = 'FILINGS_CD'
        verbose_name_plural = 'FILINGS_CD'

    def __str__(self):
        return str("%s %s" % (self.filing_id, self.filing_type))


@python_2_unicode_compatible
class SmryCd(CalAccessBaseModel):
    """
    Summary totals from filings.
    """
    filing_id = models.IntegerField(
        db_column='FILING_ID',
        db_index=True,
        verbose_name='filing ID',
        help_text="Unique filing identificiation number"
    )
    amend_id = models.IntegerField(
        db_column='AMEND_ID',
        db_index=True,
        help_text="Amendment identification number. A number of 0 is the \
original filing and 1 to 999 amendments.",
        verbose_name="amendment ID"
    )
    line_item = models.CharField(
        max_length=8,
        db_column='LINE_ITEM',
        db_index=True,
        help_text="Line number of the summary total on the source form"
    )
    REC_TYPE_CHOICES = (
        ('SMRY', 'Summary'),
    )
    rec_type = models.CharField(
        max_length=4,
        db_column='REC_TYPE',
        db_index=True,
        choices=REC_TYPE_CHOICES,
        verbose_name='record type',
    )
    FORM_TYPE_CHOICES = (
        ('401A', 'Form 401 (Slate mailer organization campaign statement): \
Schedule A, payments received'),
        ('401B', 'Form 401 (Slate mailer organization campaign statement): \
Schedule B, payments made'),
        ('A', ''),
        ('B1', ''),
        ('C', ''),
        ('D', ''),
        ('E', ''),
        ('F', ''),
        ('F401', 'Form 401 (Slate mailer organization campaign statement)'),
        ('F450', 'Form 450 (Recipient committee campaign statement, \
short form)'),
        ('F460', 'Form 460 (Recipient committee campaign statement)'),
        ('F461', 'Form 461 (Independent expenditure and major donor \
committee campaign statement)'),
        ('F465', 'Form 465 ()'),
        ('F625', 'Form 625 (Report of lobbying firm)'),
        ('F625P2', 'Form 625 (Report of lobbying firm): \
Part 2, payments received in connection with lobbying activity'),
        ('F625P3A', 'Form 625 (Report of lobbying firm): \
Part 3A, payments for activity expenses made in connection with \
lobbying activities'),
        ('F625P3B', 'Form 625 (Report of lobbying firm): \
Part 3B, payments to other lobbying firms made in connection with \
lobbying activities'),
        ('F635', 'Form 635 (Report of lobbyist employer and lobbying \
coalition)'),
        ('F635P3A', 'Form 635 (Report of lobbyist employer and lobbying \
coalition): Part 3A, payments in in-house employee lobbyists'),
        ('F635P3B', 'Form 635 (Report of lobbyist employer and lobbying \
coalition): Part 3B, payments to lobbying firms'),
        ('F635P3C', 'Form 635 (Report of lobbyist employer and lobbying \
coalition): Part 3C, activity expenses'),
        ('F635P3D', 'Form 635 (Report of lobbyist employer and lobbying \
coalition): Part 3D, other payments to influence legislative or \
administrative action'),
        ('F635P3E', 'Form 635 (Report of lobbyist employer and lobbying \
coalition): Part 3E, payments in connection with administrative testimony \
in ratemaking proceedings before the California Public Utilities Commission'),
        ('F645', 'Form 645 (Report of person spending $5,000 or more to \
influence legislative or administrative action)'),
        ('F645P2A', 'Form 645 (Report of person spending $5,000 or more to \
influence legislative or administrative action): Part 2A, activity expenses'),
        ('F645P2B', 'Form 645 (Report of person spending $5,000 or more to \
influence legislative or administrative action): Part 2B, \
other payments to influence legislative or administrative action'),
        ('F645P2C', 'Form 645 (Report of person spending $5,000 or more to \
influence legislative or administrative action): Part 2C, \
payments in connection with administrative testimony in ratemaking \
proceedings before the California Public Utilities Commission'),
        ('F900', 'Form 900 (Form 900 (Public Employee\'s Retirement Board \
         Candidate Campaign Statement)'),
        ('G', ''),
        ('H', ''),
        ('H1', ''),
        ('H2', ''),
        ('H3', ''),
        ('I', ''),
        ('S640', ''),
    )
    form_type = models.CharField(
        max_length=8,
        db_column='FORM_TYPE',
        db_index=True,
        choices=FORM_TYPE_CHOICES,
        help_text='Name of the source filing form or schedule'
    )
    amount_a = models.DecimalField(
        decimal_places=2,
        null=True,
        max_digits=14,
        db_column='AMOUNT_A',
        blank=True,
        help_text='Summary amount from column A',
        verbose_name='amount A'
    )
    amount_b = models.DecimalField(
        decimal_places=2,
        null=True,
        max_digits=14,
        db_column='AMOUNT_B',
        blank=True,
        help_text='Summary amount from column B',
        verbose_name='amount B'
    )
    amount_c = models.DecimalField(
        decimal_places=2,
        null=True,
        max_digits=14,
        db_column='AMOUNT_C',
        blank=True,
        help_text='Summary amount from column C',
        verbose_name='amount C'
    )
    elec_dt = models.DateField(
        db_column='ELEC_DT',
        null=True,
        blank=True,
        verbose_name='election date'
    )

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'SMRY_CD'
        verbose_name = 'SMRY_CD'
        verbose_name_plural = 'SMRY_CD'

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class CvrE530Cd(CalAccessBaseModel):
    """
    This table method is undocumented in the print docs.
    """
    filing_id = models.IntegerField(
        db_column='FILING_ID',
        db_index=True,
        verbose_name='filing ID',
        help_text="Unique filing identificiation number"
    )
    amend_id = models.IntegerField(
        db_column='AMEND_ID',
        db_index=True,
        help_text="Amendment identification number. A number of 0 is the \
original filing and 1 to 999 amendments.",
        verbose_name="amendment ID"
    )
    rec_type = models.CharField(db_column='REC_TYPE', max_length=3)
    form_type = models.CharField(
        db_column='FORM_TYPE',
        max_length=4,
        help_text='Name of the source filing form or schedule'
    )
    ENTITY_CODE_CHOICES = (
        # Defined here:
        # http://www.documentcloud.org/documents/1308003-cal-access-cal-\
        # format.html#document/p9
        ('', 'Unknown'),
    )
    entity_cd = models.CharField(
        db_column='ENTITY_CD',
        max_length=32,
        blank=True,
        verbose_name='entity code',
        choices=ENTITY_CODE_CHOICES
    )
    filer_naml = models.CharField(db_column='FILER_NAML', max_length=200)
    filer_namf = models.CharField(
        db_column='FILER_NAMF', max_length=4, blank=True
    )
    filer_namt = models.CharField(
        db_column='FILER_NAMT', max_length=32, blank=True
    )
    filer_nams = models.CharField(
        db_column='FILER_NAMS', max_length=32, blank=True
    )
    report_num = models.CharField(
        db_column='REPORT_NUM', max_length=32, blank=True
    )
    rpt_date = models.DateField(db_column='RPT_DATE', null=True)
    filer_city = models.CharField(
        db_column='FILER_CITY', max_length=16, blank=True
    )
    filer_st = models.CharField(db_column='FILER_ST', max_length=4, blank=True)
    filer_zip4 = models.CharField(
        db_column='FILER_ZIP4', max_length=10, blank=True
    )
    occupation = models.CharField(
        db_column='OCCUPATION', max_length=15, blank=True
    )
    employer = models.CharField(
        db_column='EMPLOYER', max_length=13, blank=True
    )
    cand_naml = models.CharField(db_column='CAND_NAML', max_length=46)
    cand_namf = models.CharField(
        db_column='CAND_NAMF', max_length=21, blank=True
    )
    cand_namt = models.CharField(
        db_column='CAND_NAMT', max_length=32, blank=True
    )
    cand_nams = models.CharField(
        db_column='CAND_NAMS', max_length=32, blank=True
    )
    district_cd = models.IntegerField(db_column='DISTRICT_CD')
    office_cd = models.IntegerField(db_column='OFFICE_CD')
    pmnt_dt = models.DateField(db_column='PMNT_DT', null=True)
    pmnt_amount = models.FloatField(db_column='PMNT_AMOUNT')
    type_literature = models.IntegerField(db_column='TYPE_LITERATURE')
    type_printads = models.IntegerField(db_column='TYPE_PRINTADS')
    type_radio = models.IntegerField(db_column='TYPE_RADIO')
    type_tv = models.IntegerField(db_column='TYPE_TV')
    type_it = models.IntegerField(db_column='TYPE_IT')
    type_billboards = models.IntegerField(db_column='TYPE_BILLBOARDS')
    type_other = models.IntegerField(db_column='TYPE_OTHER')
    other_desc = models.CharField(db_column='OTHER_DESC', max_length=49)

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'CVR_E530_CD'
        verbose_name = 'CVR_E530_CD'
        verbose_name_plural = 'CVR_E530_CD'

    def __str__(self):
        return str(self.filing_id)


@python_2_unicode_compatible
class TextMemoCd(CalAccessBaseModel):
    """
    This table contains all text memos attached to electronic filings.
    """
    filing_id = models.IntegerField(
        db_column='FILING_ID',
        db_index=True,
        verbose_name='filing ID',
        help_text="Unique filing identificiation number"
    )
    amend_id = models.IntegerField(
        db_column='AMEND_ID',
        db_index=True,
        help_text="Amendment identification number. A number of 0 is the \
original filing and 1 to 999 amendments.",
        verbose_name="amendment ID"
    )
    line_item = models.IntegerField(db_column='LINE_ITEM')
    rec_type = models.CharField(db_column='REC_TYPE', max_length=4)
    form_type = models.CharField(
        db_column='FORM_TYPE',
        max_length=8,
        help_text='Name of the source filing form or schedule'
    )
    ref_no = models.CharField(db_column='REF_NO', max_length=20, blank=True)
    text4000 = models.CharField(
        db_column='TEXT4000',
        max_length=4000, blank=True
    )

    class Meta:
        app_label = 'calaccess_raw'
        db_table = 'TEXT_MEMO_CD'
        verbose_name = 'TEXT_MEMO_CD'
        verbose_name_plural = 'TEXT_MEMO_CD'

    def __str__(self):
        return str(self.filing_id)
