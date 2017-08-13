
# Shell python helper-utility


## Usage:

```bash
$ shellu set ha 1

$ shellu list
#out: ha - 1

$ shellu get ha
#out: 1

$ shellu set test "string test" blah

$ shellu get test
#out: ['string test', 'blah']

$ shellu get test 0
#out: ['string test']

$ shellu set-index test 1 bye
$ shellu get test
#out: ['string test', 'bye']

$ shellu append test 54
#out: ['string test', 'bye', '54']


$ shellu set-many name bob age 35
#out:
#name - bob
#age - 35

$ shellu unset bob
#bob is removed

$ shellu set test "py: 3+5"
#out: 8

$ NAME='test'
$ shellu set lower_name "py: '$NAME'.lower()"

$ lines=`cat /proc/cpuinfo`
$ shellu set liens "py: '$lines'.split('\n')"


$ shellu set lines "py: sh.cat('/proc/cpuinfo').split('\n')"

