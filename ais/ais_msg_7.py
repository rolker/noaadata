#!/usr/bin/env python

"""Functions to serialize/deserialize binary messages.

Need to then wrap these functions with the outer AIS packet and then
convert the whole binary blob to a NMEA string.  Those functions are
not currently provided in this file.

serialize: python to ais binary
deserialize: ais binary to python

The generated code uses translators.py, binary.py, and aisstring.py
which should be packaged with the resulting files.

TODO(schwehr): Put in a description of the message here with fields and types.
"""
import doctest
import sys
from decimal import Decimal
import unittest

from aisutils.BitVector import BitVector

from aisutils import aisstring
from aisutils import binary
from aisutils import sqlhelp
from aisutils import uscg


fieldList = (
    'MessageID',
    'RepeatIndicator',
    'UserID',
    'Spare',
    'DestID1',
    'SeqID1',
    'DestID2',
    'SeqID2',
    'DestID3',
    'SeqID3',
    'DestID4',
    'SeqID4',
)

fieldListPostgres = (
    'MessageID',
    'RepeatIndicator',
    'UserID',
    'Spare',
    'DestID1',
    'SeqID1',
    'DestID2',
    'SeqID2',
    'DestID3',
    'SeqID3',
    'DestID4',
    'SeqID4',
)

toPgFields = {
}
"""
Go to the Postgis field names from the straight field name
"""

fromPgFields = {
}
"""
Go from the Postgis field names to the straight field name
"""

pgTypes = {
}
"""
Lookup table for each postgis field name to get its type.
"""

def encode(params, validate=False):
    '''Create a binack binary message payload to pack into an AIS Msg binack.

    Fields in params:
      - MessageID(uint): AIS message number.  Must be 7 (field automatically set to "7")
      - RepeatIndicator(uint): Indicated how many times a message has been repeated
      - UserID(uint): Unique ship identification number (MMSI).  Also known as the Source ID
      - Spare(uint): Not used.  Should be set to zero. (field automatically set to "0")
      - DestID1(uint): MMSI destication to ACK
      - SeqID1(uint): Sequence ID of the message to be acknowledged
      - DestID2(uint): MMSI destication to ACK
      - SeqID2(uint): Sequence ID of the message to be acknowledged
      - DestID3(uint): MMSI destication to ACK
      - SeqID3(uint): Sequence ID of the message to be acknowledged
      - DestID4(uint): MMSI destication to ACK
      - SeqID4(uint): Sequence ID of the message to be acknowledged
    @param params: Dictionary of field names/values.  Throws a ValueError exception if required is missing
    @param validate: Set to true to cause checking to occur.  Runs slower.  FIX: not implemented.
    @rtype: BitVector
    @return: encoded binary message (for binary messages, this needs to be wrapped in a msg 8
    @note: The returned bits may not be 6 bit aligned.  It is up to you to pad out the bits.
    '''

    bvList = []
    bvList.append(binary.setBitVectorSize(BitVector(intVal=7),6))
    if 'RepeatIndicator' in params:
        bvList.append(binary.setBitVectorSize(BitVector(intVal=params['RepeatIndicator']),2))
    else:
        bvList.append(binary.setBitVectorSize(BitVector(intVal=0),2))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['UserID']),30))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=0),2))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['DestID1']),30))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['SeqID1']),2))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['DestID2']),30))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['SeqID2']),2))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['DestID3']),30))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['SeqID3']),2))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['DestID4']),30))
    bvList.append(binary.setBitVectorSize(BitVector(intVal=params['SeqID4']),2))

    return binary.joinBV(bvList)

def decode(bv, validate=False):
    '''Unpack a binack message.

    Fields in params:
      - MessageID(uint): AIS message number.  Must be 7 (field automatically set to "7")
      - RepeatIndicator(uint): Indicated how many times a message has been repeated
      - UserID(uint): Unique ship identification number (MMSI).  Also known as the Source ID
      - Spare(uint): Not used.  Should be set to zero. (field automatically set to "0")
      - DestID1(uint): MMSI destication to ACK
      - SeqID1(uint): Sequence ID of the message to be acknowledged
      - DestID2(uint): MMSI destication to ACK
      - SeqID2(uint): Sequence ID of the message to be acknowledged
      - DestID3(uint): MMSI destication to ACK
      - SeqID3(uint): Sequence ID of the message to be acknowledged
      - DestID4(uint): MMSI destication to ACK
      - SeqID4(uint): Sequence ID of the message to be acknowledged
    @type bv: BitVector
    @param bv: Bits defining a message
    @param validate: Set to true to cause checking to occur.  Runs slower.  FIX: not implemented.
    @rtype: dict
    @return: params
    '''

    #Would be nice to check the bit count here..
    #if validate:
    #    assert (len(bv)==FIX: SOME NUMBER)
    r = {}
    r['MessageID']=7
    r['RepeatIndicator']=int(bv[6:8])
    r['UserID']=int(bv[8:38])
    r['Spare']=0
    r['DestID1']=int(bv[40:70])
    r['SeqID1']=int(bv[70:72])
    r['DestID2']=int(bv[72:102])
    r['SeqID2']=int(bv[102:104])
    r['DestID3']=int(bv[104:134])
    r['SeqID3']=int(bv[134:136])
    r['DestID4']=int(bv[136:166])
    r['SeqID4']=int(bv[166:168])
    return r

def decodeMessageID(bv, validate=False):
    return 7

def decodeRepeatIndicator(bv, validate=False):
    return int(bv[6:8])

def decodeUserID(bv, validate=False):
    return int(bv[8:38])

def decodeSpare(bv, validate=False):
    return 0

def decodeDestID1(bv, validate=False):
    return int(bv[40:70])

def decodeSeqID1(bv, validate=False):
    return int(bv[70:72])

def decodeDestID2(bv, validate=False):
    return int(bv[72:102])

def decodeSeqID2(bv, validate=False):
    return int(bv[102:104])

def decodeDestID3(bv, validate=False):
    return int(bv[104:134])

def decodeSeqID3(bv, validate=False):
    return int(bv[134:136])

def decodeDestID4(bv, validate=False):
    return int(bv[136:166])

def decodeSeqID4(bv, validate=False):
    return int(bv[166:168])


def printHtml(params, out=sys.stdout):
        out.write("<h3>binack</h3>\n")
        out.write("<table border=\"1\">\n")
        out.write("<tr bgcolor=\"orange\">\n")
        out.write("<th align=\"left\">Field Name</th>\n")
        out.write("<th align=\"left\">Type</th>\n")
        out.write("<th align=\"left\">Value</th>\n")
        out.write("<th align=\"left\">Value in Lookup Table</th>\n")
        out.write("<th align=\"left\">Units</th>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>MessageID</td>\n")
        out.write("<td>uint</td>\n")
        if 'MessageID' in params:
            out.write("    <td>"+str(params['MessageID'])+"</td>\n")
            out.write("    <td>"+str(params['MessageID'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>RepeatIndicator</td>\n")
        out.write("<td>uint</td>\n")
        if 'RepeatIndicator' in params:
            out.write("    <td>"+str(params['RepeatIndicator'])+"</td>\n")
            if str(params['RepeatIndicator']) in RepeatIndicatorDecodeLut:
                out.write("<td>"+RepeatIndicatorDecodeLut[str(params['RepeatIndicator'])]+"</td>")
            else:
                out.write("<td><i>Missing LUT entry</i></td>")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>UserID</td>\n")
        out.write("<td>uint</td>\n")
        if 'UserID' in params:
            out.write("    <td>"+str(params['UserID'])+"</td>\n")
            out.write("    <td>"+str(params['UserID'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>Spare</td>\n")
        out.write("<td>uint</td>\n")
        if 'Spare' in params:
            out.write("    <td>"+str(params['Spare'])+"</td>\n")
            out.write("    <td>"+str(params['Spare'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>DestID1</td>\n")
        out.write("<td>uint</td>\n")
        if 'DestID1' in params:
            out.write("    <td>"+str(params['DestID1'])+"</td>\n")
            out.write("    <td>"+str(params['DestID1'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>SeqID1</td>\n")
        out.write("<td>uint</td>\n")
        if 'SeqID1' in params:
            out.write("    <td>"+str(params['SeqID1'])+"</td>\n")
            out.write("    <td>"+str(params['SeqID1'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>DestID2</td>\n")
        out.write("<td>uint</td>\n")
        if 'DestID2' in params:
            out.write("    <td>"+str(params['DestID2'])+"</td>\n")
            out.write("    <td>"+str(params['DestID2'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>SeqID2</td>\n")
        out.write("<td>uint</td>\n")
        if 'SeqID2' in params:
            out.write("    <td>"+str(params['SeqID2'])+"</td>\n")
            out.write("    <td>"+str(params['SeqID2'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>DestID3</td>\n")
        out.write("<td>uint</td>\n")
        if 'DestID3' in params:
            out.write("    <td>"+str(params['DestID3'])+"</td>\n")
            out.write("    <td>"+str(params['DestID3'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>SeqID3</td>\n")
        out.write("<td>uint</td>\n")
        if 'SeqID3' in params:
            out.write("    <td>"+str(params['SeqID3'])+"</td>\n")
            out.write("    <td>"+str(params['SeqID3'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>DestID4</td>\n")
        out.write("<td>uint</td>\n")
        if 'DestID4' in params:
            out.write("    <td>"+str(params['DestID4'])+"</td>\n")
            out.write("    <td>"+str(params['DestID4'])+"</td>\n")
        out.write("</tr>\n")
        out.write("\n")
        out.write("<tr>\n")
        out.write("<td>SeqID4</td>\n")
        out.write("<td>uint</td>\n")
        if 'SeqID4' in params:
            out.write("    <td>"+str(params['SeqID4'])+"</td>\n")
            out.write("    <td>"+str(params['SeqID4'])+"</td>\n")
        out.write("</tr>\n")
        out.write("</table>\n")

def printFields(params, out=sys.stdout, format='std', fieldList=None, dbType='postgres'):
    '''Print a binack message to stdout.

    Fields in params:
      - MessageID(uint): AIS message number.  Must be 7 (field automatically set to "7")
      - RepeatIndicator(uint): Indicated how many times a message has been repeated
      - UserID(uint): Unique ship identification number (MMSI).  Also known as the Source ID
      - Spare(uint): Not used.  Should be set to zero. (field automatically set to "0")
      - DestID1(uint): MMSI destication to ACK
      - SeqID1(uint): Sequence ID of the message to be acknowledged
      - DestID2(uint): MMSI destication to ACK
      - SeqID2(uint): Sequence ID of the message to be acknowledged
      - DestID3(uint): MMSI destication to ACK
      - SeqID3(uint): Sequence ID of the message to be acknowledged
      - DestID4(uint): MMSI destication to ACK
      - SeqID4(uint): Sequence ID of the message to be acknowledged
    @param params: Dictionary of field names/values.
    @param out: File like object to write to.
    @rtype: stdout
    @return: text to out
    '''

    if 'std'==format:
        out.write("binack:\n")
        if 'MessageID' in params: out.write("    MessageID:        "+str(params['MessageID'])+"\n")
        if 'RepeatIndicator' in params: out.write("    RepeatIndicator:  "+str(params['RepeatIndicator'])+"\n")
        if 'UserID' in params: out.write("    UserID:           "+str(params['UserID'])+"\n")
        if 'Spare' in params: out.write("    Spare:            "+str(params['Spare'])+"\n")
        if 'DestID1' in params: out.write("    DestID1:          "+str(params['DestID1'])+"\n")
        if 'SeqID1' in params: out.write("    SeqID1:           "+str(params['SeqID1'])+"\n")
        if 'DestID2' in params: out.write("    DestID2:          "+str(params['DestID2'])+"\n")
        if 'SeqID2' in params: out.write("    SeqID2:           "+str(params['SeqID2'])+"\n")
        if 'DestID3' in params: out.write("    DestID3:          "+str(params['DestID3'])+"\n")
        if 'SeqID3' in params: out.write("    SeqID3:           "+str(params['SeqID3'])+"\n")
        if 'DestID4' in params: out.write("    DestID4:          "+str(params['DestID4'])+"\n")
        if 'SeqID4' in params: out.write("    SeqID4:           "+str(params['SeqID4'])+"\n")
        elif 'csv'==format:
                if None == options.fieldList:
                        options.fieldList = fieldList
                needComma = False;
                for field in fieldList:
                        if needComma: out.write(',')
                        needComma = True
                        if field in params:
                                out.write(str(params[field]))
                        # else: leave it empty
                out.write("\n")
    elif 'html'==format:
        printHtml(params,out)
    elif 'sql'==format:
                sqlInsertStr(params,out,dbType=dbType)
    else:
        print "ERROR: unknown format:",format
        assert False

    return # Nothing to return

RepeatIndicatorEncodeLut = {
    'default':'0',
    'do not repeat any more':'3',
    } #RepeatIndicatorEncodeLut

RepeatIndicatorDecodeLut = {
    '0':'default',
    '3':'do not repeat any more',
    } # RepeatIndicatorEncodeLut

######################################################################
# SQL SUPPORT
######################################################################

dbTableName='binack'
'Database table name'

def sqlCreateStr(outfile=sys.stdout, fields=None, extraFields=None
                ,addCoastGuardFields=True
                ,dbType='postgres'
                ):
        """
        Return the SQL CREATE command for this message type
        @param outfile: file like object to print to.
        @param fields: which fields to put in the create.  Defaults to all.
        @param extraFields: A sequence of tuples containing (name,sql type) for additional fields
        @param addCoastGuardFields: Add the extra fields that come after the NMEA check some from the USCG N-AIS format
        @param dbType: Which flavor of database we are using so that the create is tailored ('sqlite' or 'postgres')
        @type addCoastGuardFields: bool
        @return: sql create string
        @rtype: str

        @see: sqlCreate
        """
        # FIX: should this sqlCreate be the same as in LaTeX (createFuncName) rather than hard coded?
        outfile.write(str(sqlCreate(fields,extraFields,addCoastGuardFields,dbType=dbType)))

def sqlCreate(fields=None, extraFields=None, addCoastGuardFields=True, dbType='postgres'):
    """Return the sqlhelp object to create the table.

    @param fields: which fields to put in the create.  Defaults to all.
    @param extraFields: A sequence of tuples containing (name,sql type) for additional fields
    @param addCoastGuardFields: Add the extra fields that come after the NMEA check some from the USCG N-AIS format
    @type addCoastGuardFields: bool
    @param dbType: Which flavor of database we are using so that the create is tailored ('sqlite' or 'postgres')
    @return: An object that can be used to generate a return
    @rtype: sqlhelp.create
    """
    if fields is None:
        fields = fieldList
    c = sqlhelp.create('binack',dbType=dbType)
    c.addPrimaryKey()
    if 'MessageID' in fields: c.addInt ('MessageID')
    if 'RepeatIndicator' in fields: c.addInt ('RepeatIndicator')
    if 'UserID' in fields: c.addInt ('UserID')
    if 'Spare' in fields: c.addInt ('Spare')
    if 'DestID1' in fields: c.addInt ('DestID1')
    if 'SeqID1' in fields: c.addInt ('SeqID1')
    if 'DestID2' in fields: c.addInt ('DestID2')
    if 'SeqID2' in fields: c.addInt ('SeqID2')
    if 'DestID3' in fields: c.addInt ('DestID3')
    if 'SeqID3' in fields: c.addInt ('SeqID3')
    if 'DestID4' in fields: c.addInt ('DestID4')
    if 'SeqID4' in fields: c.addInt ('SeqID4')

    if addCoastGuardFields:
        # c.addInt('cg_s_rssi')  # Relative signal strength indicator
        # c.addInt('cg_d_strength')  # dBm receive strength
        # c.addVarChar('cg_x',10)  # Idonno
        c.addInt('cg_t_arrival')  # Receive timestamp from the AIS equipment 'T'
        c.addInt('cg_s_slotnum')  # Slot received in
        c.addVarChar('cg_r',15)  # Receiver station ID  -  should usually be an MMSI, but sometimes is a string
        c.addInt('cg_sec')  # UTC seconds since the epoch

        c.addTimestamp('cg_timestamp') # UTC decoded cg_sec - not actually in the data stream

    return c

def sqlInsertStr(params, outfile=sys.stdout, extraParams=None, dbType='postgres'):
        """
        Return the SQL INSERT command for this message type
        @param params: dictionary of values keyed by field name
        @param outfile: file like object to print to.
        @param extraParams: A sequence of tuples containing (name,sql type) for additional fields
        @return: sql create string
        @rtype: str

        @see: sqlCreate
        """
        outfile.write(str(sqlInsert(params,extraParams,dbType=dbType)))


def sqlInsert(params,extraParams=None,dbType='postgres'):
        """
        Give the SQL INSERT statement
        @param params: dict keyed by field name of values
        @param extraParams: any extra fields that you have created beyond the normal ais message fields
        @rtype: sqlhelp.insert
        @return: insert class instance
         TODO(schwehr):allow optional type checking of params?
        @warning: this will take invalid keys happily and do what???
        """

        i = sqlhelp.insert('binack',dbType=dbType)

        if dbType=='postgres':
                finished = []
                for key in params:
                        if key in finished:
                                continue

                        if key not in toPgFields and key not in fromPgFields:
                                if type(params[key])==Decimal: i.add(key,float(params[key]))
                                else: i.add(key,params[key])
                        else:
                                if key in fromPgFields:
                                        val = params[key]
                                        # Had better be a WKT type like POINT(-88.1 30.321)
                                        i.addPostGIS(key,val)
                                        finished.append(key)
                                else:
                                        # Need to construct the type.
                                        pgName = toPgFields[key]
                                        #valStr='GeomFromText(\''+pgTypes[pgName]+'('
                                        valStr=pgTypes[pgName]+'('
                                        vals = []
                                        for nonPgKey in fromPgFields[pgName]:
                                                vals.append(str(params[nonPgKey]))
                                                finished.append(nonPgKey)
                                        valStr+=' '.join(vals)+')'
                                        i.addPostGIS(pgName,valStr)
        else:
                for key in params:
                        if type(params[key])==Decimal: i.add(key,float(params[key]))
                        else: i.add(key,params[key])

        if None != extraParams:
                for key in extraParams:
                        i.add(key,extraParams[key])

        return i

######################################################################
# LATEX SUPPORT
######################################################################

def latexDefinitionTable(outfile=sys.stdout
                ):
        """
        Return the LaTeX definition table for this message type
        @param outfile: file like object to print to.
        @type outfile: file obj
        @return: LaTeX table string via the outfile
        @rtype: str

        """
        o = outfile

        o.write("""
\\begin{table}%[htb]
\\centering
\\begin{tabular}{|l|c|l|}
\\hline
Parameter & Number of bits & Description
\\\\  \\hline\\hline
MessageID & 6 & AIS message number.  Must be 7 \\\\ \hline
RepeatIndicator & 2 & Indicated how many times a message has been repeated \\\\ \hline
UserID & 30 & Unique ship identification number (MMSI).  Also known as the Source ID \\\\ \hline
Spare & 2 & Not used.  Should be set to zero. \\\\ \hline
DestID1 & 30 & MMSI destication to ACK \\\\ \hline
SeqID1 & 2 & Sequence ID of the message to be acknowledged \\\\ \hline
DestID2 & 30 & MMSI destication to ACK \\\\ \hline
SeqID2 & 2 & Sequence ID of the message to be acknowledged \\\\ \hline
DestID3 & 30 & MMSI destication to ACK \\\\ \hline
SeqID3 & 2 & Sequence ID of the message to be acknowledged \\\\ \hline
DestID4 & 30 & MMSI destication to ACK \\\\ \hline
SeqID4 & 2 & Sequence ID of the message to be acknowledged\\\\ \\hline \\hline
Total bits & 168 & Appears to take 1 slot \\\\ \\hline
\\end{tabular}
\\caption{AIS message number 7: Binary acknowledgement of addressed message}
\\label{tab:binack}
\\end{table}
""")

######################################################################
# Text Definition
######################################################################

def textDefinitionTable(outfile=sys.stdout ,delim='    '):
    """Return the text definition table for this message type

    @param outfile: file like object to print to.
    @type outfile: file obj
    @return: text table string via the outfile
    @rtype: str

    """
    o = outfile
    o.write('Parameter'+delim+'Number of bits'+delim+"""Description
MessageID"""+delim+'6'+delim+"""AIS message number.  Must be 7
RepeatIndicator"""+delim+'2'+delim+"""Indicated how many times a message has been repeated
UserID"""+delim+'30'+delim+"""Unique ship identification number (MMSI).  Also known as the Source ID
Spare"""+delim+'2'+delim+"""Not used.  Should be set to zero.
DestID1"""+delim+'30'+delim+"""MMSI destication to ACK
SeqID1"""+delim+'2'+delim+"""Sequence ID of the message to be acknowledged
DestID2"""+delim+'30'+delim+"""MMSI destication to ACK
SeqID2"""+delim+'2'+delim+"""Sequence ID of the message to be acknowledged
DestID3"""+delim+'30'+delim+"""MMSI destication to ACK
SeqID3"""+delim+'2'+delim+"""Sequence ID of the message to be acknowledged
DestID4"""+delim+'30'+delim+"""MMSI destication to ACK
SeqID4"""+delim+'2'+delim+"""Sequence ID of the message to be acknowledged
Total bits"""+delim+"""168"""+delim+"""Appears to take 1 slot""")


######################################################################
# UNIT TESTING
######################################################################
def testParams():
    '''Return a params file base on the testvalue tags.
    @rtype: dict
    @return: params based on testvalue tags
    '''
    params = {}
    params['MessageID'] = 7
    params['RepeatIndicator'] = 1
    params['UserID'] = 1193046
    params['Spare'] = 0
    params['DestID1'] = 1193001
    params['SeqID1'] = 1
    params['DestID2'] = 1193002
    params['SeqID2'] = 2
    params['DestID3'] = 1193003
    params['SeqID3'] = 3
    params['DestID4'] = 1193004
    params['SeqID4'] = 0

    return params

class Testbinack(unittest.TestCase):
    '''Use testvalue tag text from each type to build test case the binack message'''
    def testEncodeDecode(self):

        params = testParams()
        bits   = encode(params)
        r      = decode(bits)

        # Check that each parameter came through ok.
        self.failUnlessEqual(r['MessageID'],params['MessageID'])
        self.failUnlessEqual(r['RepeatIndicator'],params['RepeatIndicator'])
        self.failUnlessEqual(r['UserID'],params['UserID'])
        self.failUnlessEqual(r['Spare'],params['Spare'])
        self.failUnlessEqual(r['DestID1'],params['DestID1'])
        self.failUnlessEqual(r['SeqID1'],params['SeqID1'])
        self.failUnlessEqual(r['DestID2'],params['DestID2'])
        self.failUnlessEqual(r['SeqID2'],params['SeqID2'])
        self.failUnlessEqual(r['DestID3'],params['DestID3'])
        self.failUnlessEqual(r['SeqID3'],params['SeqID3'])
        self.failUnlessEqual(r['DestID4'],params['DestID4'])
        self.failUnlessEqual(r['SeqID4'],params['SeqID4'])

def addMsgOptions(parser):
    parser.add_option('-d','--decode',dest='doDecode',default=False,action='store_true',
                help='decode a "binack" AIS message')
    parser.add_option('-e','--encode',dest='doEncode',default=False,action='store_true',
                help='encode a "binack" AIS message')
    parser.add_option('--RepeatIndicator-field', dest='RepeatIndicatorField',default=0,metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--UserID-field', dest='UserIDField',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--DestID1-field', dest='DestID1Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--SeqID1-field', dest='SeqID1Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--DestID2-field', dest='DestID2Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--SeqID2-field', dest='SeqID2Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--DestID3-field', dest='DestID3Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--SeqID3-field', dest='SeqID3Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--DestID4-field', dest='DestID4Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')
    parser.add_option('--SeqID4-field', dest='SeqID4Field',metavar='uint',type='int'
        ,help='Field parameter value [default: %default]')

def main():
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options]")

    parser.add_option('--doc-test',dest='doctest',default=False,action='store_true',
        help='run the documentation tests')
    parser.add_option('--unit-test',dest='unittest',default=False,action='store_true',
        help='run the unit tests')
    parser.add_option('-v','--verbose',dest='verbose',default=False,action='store_true',
        help='Make the test output verbose')

    # FIX: remove nmea from binary messages.  No way to build the whole packet?
    # FIX: or build the surrounding msg 8 for a broadcast?
    typeChoices = ('binary','nmeapayload','nmea') # FIX: what about a USCG type message?
    parser.add_option('-t', '--type', choices=typeChoices, type='choice',
        dest='ioType', default='nmeapayload',
        help='What kind of string to write for encoding ('+', '.join(typeChoices)+') [default: %default]')


    outputChoices = ('std','html','csv','sql' )
    parser.add_option('-T', '--output-type', choices=outputChoices,
        type='choice', dest='outputType', default='std',
        help='What kind of string to output ('+', '.join(outputChoices)+') '
        '[default: %default]')

    parser.add_option('-o','--output',dest='outputFileName',default=None,
        help='Name of the python file to write [default: stdout]')

    parser.add_option('-f', '--fields', dest='fieldList', default=None,
        action='append', choices=fieldList,
        help='Which fields to include in the output.  Currently only for csv '
        'output [default: all]')

    parser.add_option('-p', '--print-csv-field-list', dest='printCsvfieldList',
        default=False,action='store_true',
        help='Print the field name for csv')

    parser.add_option('-c', '--sql-create', dest='sqlCreate', default=False,
        action='store_true',
        help='Print out an sql create command for the table.')

    parser.add_option('--latex-table', dest='latexDefinitionTable',
        default=False,action='store_true',
        help='Print a LaTeX table of the type')

    parser.add_option('--text-table', dest='textDefinitionTable', default=False,
        action='store_true',
        help='Print delimited table of the type (for Word table importing)')

    parser.add_option('--delimt-text-table', dest='delimTextDefinitionTable',
        default='    ',
        help='Delimiter for text table [default: \'%default\'] '
        '(for Word table importing)')

    dbChoices = ('sqlite','postgres')
    parser.add_option('-D', '--db-type', dest='dbType', default='postgres',
        choices=dbChoices,type='choice',
        help='What kind of database ('+', '.join(dbChoices)+') '
        '[default: %default]')

    addMsgOptions(parser)

    (options,args) = parser.parse_args()
    success = True

    if options.doctest:
            import os; print os.path.basename(sys.argv[0]), 'doctests ...',
            sys.argv = [sys.argv[0]]
            if options.verbose:
              sys.argv.append('-v')

            numfail, numtests = doctest.testmod()
            if not numfail:
                print 'ok'
            else:
                print 'FAILED'
                success = False

    if not success: sys.exit('Something Failed')
    del success # Hide success from epydoc

    if options.unittest:
            sys.argv = [sys.argv[0]]
            if options.verbose: sys.argv.append('-v')
            unittest.main()

    outfile = sys.stdout
    if None!=options.outputFileName:
            outfile = file(options.outputFileName,'w')


    if options.doEncode:
        # Make sure all non required options are specified.
        if None==options.RepeatIndicatorField: parser.error("missing value for RepeatIndicatorField")
        if None==options.UserIDField: parser.error("missing value for UserIDField")
        if None==options.DestID1Field: parser.error("missing value for DestID1Field")
        if None==options.SeqID1Field: parser.error("missing value for SeqID1Field")
        if None==options.DestID2Field: parser.error("missing value for DestID2Field")
        if None==options.SeqID2Field: parser.error("missing value for SeqID2Field")
        if None==options.DestID3Field: parser.error("missing value for DestID3Field")
        if None==options.SeqID3Field: parser.error("missing value for SeqID3Field")
        if None==options.DestID4Field: parser.error("missing value for DestID4Field")
        if None==options.SeqID4Field: parser.error("missing value for SeqID4Field")
    msgDict = {
        'MessageID': '7',
        'RepeatIndicator': options.RepeatIndicatorField,
        'UserID': options.UserIDField,
        'Spare': '0',
        'DestID1': options.DestID1Field,
        'SeqID1': options.SeqID1Field,
        'DestID2': options.DestID2Field,
        'SeqID2': options.SeqID2Field,
        'DestID3': options.DestID3Field,
        'SeqID3': options.SeqID3Field,
        'DestID4': options.DestID4Field,
        'SeqID4': options.SeqID4Field,
    }

    bits = encode(msgDict)
    if 'binary' == options.ioType:
        print str(bits)
    elif 'nmeapayload'==options.ioType:
        # FIX: figure out if this might be necessary at compile time
        bitLen=len(bits)
        if bitLen % 6 != 0:
            bits = bits + BitVector(size=(6 - (bitLen%6)))  # Pad out to multiple of 6
        print binary.bitvectoais6(bits)[0]

    # FIX: Do not emit this option for the binary message payloads.  Does not make sense.
    elif 'nmea' == options.ioType:
        nmea = uscg.create_nmea(bits)
        print nmea
    else:
        sys.exit('ERROR: unknown ioType.  Help!')


        if options.sqlCreate:
                sqlCreateStr(outfile,options.fieldList,dbType=options.dbType)

        if options.latexDefinitionTable:
                latexDefinitionTable(outfile)

        # For conversion to word tables
        if options.textDefinitionTable:
                textDefinitionTable(outfile,options.delimTextDefinitionTable)

        if options.printCsvfieldList:
                # Make a csv separated list of fields that will be displayed for csv
                if None == options.fieldList: options.fieldList = fieldList
                import StringIO
                buf = StringIO.StringIO()
                for field in options.fieldList:
                        buf.write(field+',')
                result = buf.getvalue()
                if result[-1] == ',': print result[:-1]
                else: print result

        if options.doDecode:
                if len(args)==0: args = sys.stdin
                for msg in args:
                        bv = None

                        if msg[0] in ('$','!') and msg[3:6] in ('VDM','VDO'):
                                # Found nmea
                                # FIX: do checksum
                                bv = binary.ais6tobitvec(msg.split(',')[5])
                        else: # either binary or nmeapayload... expect mostly nmeapayloads
                                # assumes that an all 0 and 1 string can not be a nmeapayload
                                binaryMsg=True
                                for c in msg:
                                        if c not in ('0','1'):
                                                binaryMsg=False
                                                break
                                if binaryMsg:
                                        bv = BitVector(bitstring=msg)
                                else: # nmeapayload
                                        bv = binary.ais6tobitvec(msg)

                        printFields(decode(bv)
                                    ,out=outfile
                                    ,format=options.outputType
                                    ,fieldList=options.fieldList
                                    ,dbType=options.dbType
                                    )

############################################################
if __name__=='__main__':
    main()
