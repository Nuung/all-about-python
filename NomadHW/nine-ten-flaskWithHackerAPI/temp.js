this.responseCallBack = function (pbSync) {
    var voResult = null;
    if (xmlHttpRequest.readyState == 4) {
        var vnStatus = xmlHttpRequest.status;
        if (vnStatus == 200) {
            debugger;
            submissionInstance.responseState = true;
            var vsResProtocolType = xmlHttpRequest.getResponseHeader(eXria.protocols.SubmissionType.RES_PROTOCOL_HEADER);

            if (vsResProtocolType == "" && page.metadata.useJsonInstance)
                vsResProtocolType = submissionInstance.resProtocol;
            var voResponseParser = eXria.protocols.ProtocolParserFactory.getResponseParser(submissionInstance, vsResProtocolType);

            if (page.metadata.useJsonInstance) {
                voResult = xmlHttpRequest.responseText;
                voResult = (voResult == "") ? voResult : eval("(" + voResult + ")");
                submissionInstance.redirectJsonLocation(voResult);
                submissionInstance.bindJsErrMsg(voResult);
                if (voResponseParser.bind) { submissionInstance.bindJsInstance(voResult); }
            }
            else {
                voResult = voResponseParser.parse(xmlHttpRequest);
                submissionInstance.redirectLocation(voResult);
                submissionInstance.bindErrMsg(voResult);
                if (voResponseParser.bind) { submissionInstance.bindInstance(voResult); }
            }