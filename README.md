# zeiss converter

is a converter that takes table files from zeiss calyso cmm and data from zeissStartGui, where the user enters data about the measurement run, and converts it into json file format and gets inserted into a mongodb instance.


Example Data
```csv
planid	partnb	id	type	idsymbol	actual	nominal	uppertol	lowertol	deviation	exceed	warningLimitCF	featureid	featuresigma	comment	link	linkmode	mmc	useruppertol	userlowertol	fftphi	fftphiunit	zoneroundnessangle	groupname	groupname2	datumAid	datumBid	datumCid	natuppertolid	natlowertolid	decimalplaces	featurePosX	featurePosY	featurePosZ	unit	group1	group2	group3	group4	group5	group6	group7	group8	group9	group10	
00469339-Gate	815	Gate_16MM_1.Seal_1_X	X1	xValue	1.0000000	0.0000000	0.0050000	-0.0050000	0.0000000		100.0000000	Gate_16MM_1.Seal_1	0.0000000					0.0050000	-0.0050000				Gate_16MM_1	Gate_16MM_1.Seal_Dia				1	1	3	-39.0000000	6.0000000	-10.1350000	mm	Gate_16MM_1	Gate_16MM_1.Seal_Dia
00469339-Gate	815	Gate_16MM_1.Seal_1_Y	Y1	yValue	0.0000000	0.0000000	0.0050000	-0.0050000	0.0000000		100.0000000	Gate_16MM_1.Seal_1	0.0000000					0.0050000	-0.0050000				Gate_16MM_1	Gate_16MM_1.Seal_Dia				1	1	3	-39.0000000	6.0000000	-10.1350000	mm	Gate_16MM_1	Gate_16MM_1.Seal_Dia
00469339-Gate	815	Gate_16MM_1.Seal_1_D	D1	diameter	16.0000000	16.0000000	0.0100000	0.0000000	0.0000000	0.0000000	100.0000000	Gate_16MM_1.Seal_1	0.0000000					0.0100000	0.0000000				Gate_16MM_1	Gate_16MM_1.Seal_Dia				1	1	3	-39.0000000	6.0000000	-10.1350000	mm	Gate_16MM_1	Gate_16MM_1.Seal_Dia
```

combining with the user supplied information

```json
{
  "Dialog": {
    "name": "BenR",
    "partID": "00275553-S6",
    "MSN": "213",
    "CAV": "",
    "xOffset": "0.0000",
    "yOffset": "0.0000",
    "zOffset": "0.0000",
    "WO": "60001725",
    "SO": "",
    "comment": "",
    "startRun": 6,
    "endRun": 0,
    "operation": "HSC",
    "tags": "",
    "status": "measured",
    "counter": 12
  },
  "Setup": {
    "nominalXoffset": "0.0000",
    "nominalYoffset": "0.0000",
    "nominalZoffset": "0.0000",
    "fileIndex": "MSN",
    "importScan": false,
    "autorun": false
  },
  "Export": ""
}
```



## Output:

```json
{
  "name": "BenR",
  "partID": "00275553-S6",
  "MSN": "213",
  "CAV": "",
  "xOffset": "0.0000",
  "yOffset": "0.0000",
  "zOffset": "0.0000",
  "WO": "60001725",
  "SO": "",
  "comment": "",
  "startRun": 6,
  "endRun": 0,
  "operation": "HSC",
  "tags": "",
  "status": "measured",
  "counter": 12,
  "chrData": [
    {
      "id": "Gate_16MM_1.Seal_1_X",
      "idtype": "xValue",
      "act": 0.001,
      "nom": 0,
      "utol": 0.005,
      "ltol": -0.005
    },
    {
      "id": "Gate_16MM_1.Seal_1_Y",
      "idtype": "yxValue",
      "act": 0.005,
      "nom": 0,
      "utol": 0.005,
      "ltol": -0.005
    },
    {
      "id": "Gate_16MM_1.Seal_1_D",
      "idtype": "diameter",
      "act": 16.001,
      "nom": 16,
      "utol": 0.005,
      "ltol": -0.005
    }
  ]
}
```







