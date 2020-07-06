Module Pollenisator.worker.crtsh.crtsh
======================================

Functions
---------

    
`format_entries(results, do_resolve_dns)`
:   Sort and deduplicate hostnames and, if DNS resolution is turned on, resolve hostname

    
`get_rss_for_domain(domain)`
:   Pull the domain identity information from crt.sh

    
`parse_entries(identity, results_list)`
:   This is pretty gross, but necessary when using crt.sh: parse the contents of the summary
    entry and return individual host names.