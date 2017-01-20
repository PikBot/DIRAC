import unittest
from mock import MagicMock
import sys
import mock

mocked_gfal2 = MagicMock()
sys.modules['gfal2'] = mocked_gfal2

from DIRAC.Resources.Storage.GFAL2_XROOTStorage import GFAL2_XROOTStorage


class XROOTStorage_TestCase( unittest.TestCase ):

  def setUp( self ):
    '''
    Setup
    '''
    # Mock external libraries / modules not interesting for the unit test


    self.parameterDict = dict( Protocol = 'protocol',
                              Path = '/path',
                              Host = 'host',
                              Port = '',
                              SvcClass = 'spaceToken',
                              WSPath = 'wspath',
                             )

  def test_constructURLFromLFN( self ):

    resource = GFAL2_XROOTStorage( 'storageName', self.parameterDict )

    resource.se = MagicMock()
    voName = "voName"
    resource.se.vo = voName
    testLFN = "/%s/path/to/filename" % voName

    # # with spaceToken
    res = resource.constructURLFromLFN( testLFN )
    self.assertTrue( res['OK'] )
    self.assertEqual( "protocol://host//path%s?svcClass=%s" % ( testLFN, self.parameterDict['SvcClass'] )
                      , res['Value'] )

    # # no spaceToken
    resource.protocolParameters['SvcClass'] = ""
    res = resource.constructURLFromLFN( testLFN )
    self.assertTrue( res['OK'] )
    self.assertEqual( "protocol://host//path%s" % ( testLFN, ) , res['Value'] )



if __name__ == '__main__':

  # Shut up the gLogger
  # Uncomment this line and comment the next 2 if you want debug
  # gLogger.setLevel( "DEBUG" )
  from DIRAC.FrameworkSystem.private.logging.Logger import Logger
  Logger.processMessage = MagicMock()


  suite = unittest.defaultTestLoader.loadTestsFromTestCase( XROOTStorage_TestCase )
  unittest.TextTestRunner( verbosity = 2 ).run( suite )
