	var input;
	var	urls = [];
	var windows = new Array();
	var timeoutId = null;
	var url;
	var refresh   = 5;
	var myWindow  = null;
	var currentURL = 0;
	var numURLs    = urls.length;
	var separate   = false;
	var toolbar    = 1;

	function doIt()
	{
		input    = prompt('Give the URLs to cycle. Split them with a , between each one','www.bbc.co.uk');
		urls = String(input).split(',');
		//alert('Status ' + windows[0] + ' and ' + windows[0].closed );
		if ( windows[0] && !windows[0].closed )
		{
			doRefresh();
		}
		else
		{
			reset();

			refresh = 5;

			separate = 0;
			toolbar  = 1;
			refresh  = prompt('Refreshing interval',50);
			for ( var i = 0; i < urls.length; i++)
			{		
				var url = urls[i];
				if(url.indexOf('http://')==-1){url='http://'+url;}		
				urls[i]=url;
			}
			if ( urls.length == 0 )
			{
				alert(urls.length + '\n' + urls);
				alert('Please enter at least 1 URL');
				return;
			}

			var answer = confirm('This page refresher must not be used for malicious purposes.\nLazyWebTools (original cycle.js) and Tipaa (bookmarkeltising it) are not responsible for your usage of this tool.\nBy hitting OK you agree to use the tool legally and you agree that you are not using this tool for malicious purposes.\n\nContinue?')
            if (!answer)
		    {
				return;
			}
			if (separate)
			{
			    for (var k=0; k<numURLs; k++)
			    {
				    windows[k] = window.open(urls[k],'mywin'+k, 'toolbar=' + toolbar + ',resizable=1,scrollbars=1'); 
			    }
			}
			else
			{
				windows[0] = window.open(urls[currentURL++],'mywin', 'toolbar=' + toolbar + ',resizable=1,scrollbars=1'); 	
			}			
			timeoutId = setTimeout( 'doRefresh()', refresh*1000 );
		}		
	}

	function doRefresh()
	{		
		clearTimeout(timeoutId);

		try
		{
			if (separate)
			{			
				for (var k=0; k<numURLs; k++)
				{
					if ( windows[k] && !windows[k].closed )
					{
						windows[k].location.href = urls[k];
					}
				}
			}
			else
			{
				if ( windows[0] && !windows[0].closed )
				{
			        if ( currentURL == numURLs )
		            {
			            currentURL = 0;
		            }
					windows[0].location.href = urls[currentURL];
					currentURL++;
				}
			}			
			timeoutId = setTimeout( 'doRefresh()', refresh*1000 );
		}
		catch(e)
		{
			// do nothing
		}		
	}
	doIt();
	function reset()
	{
		windows    = new Array();
		currentURL = 0;
		clearTimeout(timeoutId);
	}