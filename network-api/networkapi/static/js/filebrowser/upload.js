(function($, global){
    var queue = [];

    // would be nicer to return at the top, but some browsers complain about "unreachable" code
    if(!global.FormData){
        console.log('XHR file uploads are not supported. Falling back to regular uploads.');

        // replace the fancy input wrapper with a standard file input
        $(function(){
            $('#upload-form').find('.file-input-wrapper').replaceWith('<input name="Filedata" type="file" />');
        });
    }else{
        $(function(){
            var form = $('#upload-form');
            var formData = form.data();
            var doneRedirect = formData.redirectWhenDone || '/';
            var extensions = formData.allowedExtensions && formData.allowedExtensions.split(',');
            var allowedSize = formData.sizeLimit && parseInt(formData.sizeLimit);
            
            // override: start #160
            var uploadBtn = $('#upload-button');
            // override: end #160

            form.on('change', 'input[type="file"]', function(e){
                var input = this;
                $.each(input.files, function(index, selectedFile) {
                    var resultElement = $(input).closest('.file-input-wrapper').children('.file-input-result').last();
                    var status = resultElement.find('.status');
                    var hasExtensionError = !validateExtension(selectedFile, extensions);
                    var hasSizeError = !validateSize(selectedFile, allowedSize);

                    resultElement.addClass('selected');
                    
                    // override: start #160
                    uploadBtn.hide();
                    // override: end #160

                    // Add an empty result element for the next file
                    //
                    // jquery has .clone, however it has some strange behavior,
                    // like assigning id="null" to the newly-created element.
                    // maybe it's fixed in newer version but grapelli seems to be on 1.7
                    $(resultElement[0].outerHTML).removeClass('selected').insertAfter(resultElement);

                    // shows the error message if there was an error
                    if(hasExtensionError || hasSizeError) {
                        status
                            .addClass('error')
                            .text(hasSizeError ? formData.sizeError : formData.extensionError);
                    }else if(selectedFile) {
                        function resume() {
                            // display the selected file's name
                            status.removeClass('error').text(selectedFile.name);
                            resultElement.data('selectedFile', selectedFile);
                            
                            // override: start #160
                            uploadBtn.show();
                            // override: end #160
                        }

                        // sends a request to the server that checks whether the file is taken
                        checkIsTaken(form, selectedFile.name).then(resume, function(filename){
                            if(window.confirm(formData.replaceMessage + ' ' + (filename || '') + '?')){
                                resume();
                            }else{
                                resultElement.remove();
                                
                                // override: start #160
                                uploadBtn.show();
                                // override: end #160
                            }
                        });
                    }
                });
            });

            form.on('submit', function(e){
                e.preventDefault();
                var data = form.serializeArray();
                var url = form.attr('action');

                // hide the "clear queue" button, we don't
                // support cancelling of uploads yet
                $('a.deletelink').hide();

                // go through all of the inputs and add them to the queue
                $.each($('.file-input-result'), function(index, el){
                    var element = $(el);

                    // only add it to the queue if it has a selected file
                    var file = element.data('selectedFile');
                    if(file){
                        var promise = queueFile(url, data, {
                            field: 'Filedata',
                            value: file
                        });

                        // note that the file needs to be cleared so pressing
                        // "upload" doesn't trigger another upload
                        element.data('selectedFile', null);

                        var progress = element.find('.progress-inner');

                        element.removeClass('selected').addClass('in-progress');

                        // when failed, show the error message
                        promise.fail(function(){
                            element.find('.status').addClass('error').text(formData.serverError);
                        });

                        // on progress, update the progressbar
                        promise.progress(function(current){
                            var inPercent = current + '%';
                            progress.css('width', inPercent);
                            progress.attr('data-percentage', inPercent);
                        });

                        // this one should be at the bottom so it always fires last.
                        // in any case the upload should be marked as being "done"
                        promise.always(function(){
                            element.removeClass('in-progress selected').addClass('done');

                            // redirect if there's nothing left in the queue
                            if(queue.length === 0){
                                window.location.href = doneRedirect;
                            }
                        });
                    }
                });

                // if the queue is empty, redirect immediately
                if(queue.length === 0){
                    window.location.href = doneRedirect;
                }
            });

            // clears a particular item that has been selected
            form.on('click', '.cancel-button', function(){
                var element = $(this).closest('.file-input-result');

                if(element.siblings('.file-input-result').length){
                    element.remove();
                }else{
                    element
                        .removeClass('selected in-progress')
                        .data('selectedFile', null);
                }
            });

            // clears all of the selected uploads
            $('a.deletelink').click(function(e){
                e.preventDefault();

                var results = form.find('.file-input-result');
                
                $.each(results, function(index, current){
                    var result = $(current);

                    if(index + 1 === results.length){
                        result.data('selectedFile', null);
                        result.removeClass('selected in-progress done');
                    }else{
                        result.remove();
                    }
                });
            });
        });
    }

    function queueFile(url, data, file){
        var xhr = new global.XMLHttpRequest();
        var formData = new global.FormData();
        var deferred = $.Deferred();
        var sendRequest = function(){
            xhr.open('POST', url, true);
            xhr.send(formData);
        };

        // add a reference to the xhr object just in case
        // it isn't used atm but might be useful for something
        // like aborting a request that is in progress
        deferred.xhr = xhr;

        // add all of the hidden fields to the request
        $.each(data, function(index, item){
            formData.append(item.name, item.value);
        });

        // add the file to the request
        formData.append(file.field, file.value);

        xhr.addEventListener('readystatechange', function(){
            var status = xhr.status;
            var index = queue.indexOf(deferred);

            // anything different from 4 means "not-ready"
            if(xhr.readyState !== 4) return;

            // remove the deferred from the queue
            if(index > -1){
                queue.splice(index, 1);
            }

            // upload was successful
            if(status > 0 && 200 <= status && status < 300){
                deferred.notify(100);
                deferred.resolve(xhr.responseText);
            // upload failed
            }else{
                deferred.reject(status);
            }
        });

        // bear in mind that its xhr.upload, not xhr
        xhr.upload.addEventListener('progress', function(event){
            if(event.lengthComputable){
                deferred.notify((event.loaded/event.total*100).toFixed(2));
            }
        });

        // if there are other pending uploads, wait for the
        // last one to finish before starting the upload
        if(queue.length){
            queue[queue.length - 1].always(sendRequest);
        // otherwise just start
        }else{
            sendRequest();
        }

        queue.push(deferred);
        return deferred;
    }

    // checks whether the specified file's extension is allowed
    function validateExtension(file, extensions){
        if(file && extensions && extensions.length){
            var fileExtension = file.name.slice(file.name.lastIndexOf('.'), file.name.length).toLowerCase();

            if(extensions.indexOf(fileExtension) === -1){
                return false;
            }
        }

        return true;
    }

    // checks whether a file's size is under the limit
    function validateSize(file, allowed){
        if(file && allowed){
            if(typeof allowed === 'number' && !global.isNaN(allowed)){
                return file.size <= allowed;
            }

            return false;
        }

        return true;
    }

    // turns the result of jQuery's serializeArray into a proper object
    function serializeToObject(array){
        var output = {};
        var i = 0;
        var len = array.length;

        for(i; i < len; i++){
            output[array[i].name] = array[i].value;
        }

        return output;
    }

    // checks whether the supplied is empty
    function isEmpty(value){
        if(!value){
            return false;
        }else if(window.Array.isArray(value)){
            return value.length === 0;
        }else if(typeof value === 'object'){
            return window.Object.keys(value).length === 0;
        }

        return true;
    }

    // checks whether there's a file with the same name in the same folder
    function checkIsTaken(form, filename){
        var checkUrl = form.data().checkUrl;
        var isTaken = false;
        var deferred = $.Deferred();

        if(checkUrl){
            var data = serializeToObject(form.serializeArray());
            data.file = filename;

            // checks whether a file with the same filename is
            // present in the same folder. the backend returns an
            // empty object if the file is taken. otherwise it returns
            // an object like { filename: 'whatever.ext' }
            $.post(checkUrl, data).then(function(response){
                var parsed = null;

                // JSON.parse throws an error if the response
                // isn't valid JSON
                try{
                    parsed = window.JSON.parse(response);
                }catch(e){}

                isTaken = !isEmpty(parsed);

                if(isTaken){
                    deferred.reject(filename);
                }else{
                    deferred.resolve();
                }
            }, deferred.resolve);
        }else{
            deferred.resolve();
        }

        return deferred;
    }

})(jQuery, window);
