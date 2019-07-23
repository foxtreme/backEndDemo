<h1>Flask backend</h1>
<p>
There are 2 models here: Purchase and Loan, a loan has 0 or more purchases 
and a purchase is associated to a single loan. <br>
When consulting purchases you will need to pass the loan_id field in the request.
 Additionally the update methods run through the request json to update only the 
 attributes passed.
</p>
<h2> Notes: </h2>

<em>Required libraries and versions:</em> 
<ul>
    <li>python 3.7</li>
    <li>flask</li>
    <li>flask_sqlalchemy</li>
    <li>flask_marshmallow</li>
    <li>marshmallow-sqlalchemy</li>
</ul>

type the following in your console before running it:
<pre>
$python
>>> from application import db
>>> db.create_all()
</pre>

Then run it with:
<pre>
$python appplication.py
</pre>


