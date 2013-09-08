class SubdomainMiddleware:
    def process_request(self, request):
        """Parse out the subdomain from the request"""
        request.subdomain = None
        print "start"
        print request.META
        host = request.META.get('HTTP_HOST', '')
        print "host:  "+host
        host_s = host.replace('www.', '').split('.')
        print "host_s:  "+str(host_s)
        if len(host_s) > 2:
            
            request.subdomain = ''.join(host_s[:-2])
            print "subdomain is "
            print request.subdomain
