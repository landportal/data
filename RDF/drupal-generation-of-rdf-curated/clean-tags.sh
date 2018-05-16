input_file=$1
echo "running clean..."
# &lt;p&gt => <p>
sed -ie 's/&lt;p&gt;//g' $input_file
# &lt;/p&gt => </p>
sed -ie 's/&lt;\/p&gt;//g' $input_file
#Remove the href. Keep the text link
#&lt;a href="http://www.landmatrix.org/en/about/"&gt;http://www.landmatrix.org/en/about/&lt;/a&gt;
#remove the <a> tag
sed -ie 's/&lt;a.*"&gt;//g' $input_file
# remove </a> tag
sed -ie 's/&lt;\/a&gt;//g' $input_file

#Only if they are needed
# &#39; => '
#sed -ie "s/&#39;/'/g" $input_file
# &quot; => "
#sed -ie 's/&quot;/"/g' $input_file
# &amp;gt; => ->
#sed -ie 's/&amp;gt;//g' $input_file
