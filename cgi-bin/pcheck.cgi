#!/usr/bin/perl

#��������������������������������������������������������������������
#�� Perl Checker v2.21 (2002/09/07)
#�� Copyright(C) Kent Web 2002
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'PerlChecker v2.21';
#��������������������������������������������������������������������
#�� [�g�p���@]
#��   1. ���̃X�N���v�g (pcheck.cgi) ��CGI���s�\�ȃf�B���N�g����
#��      �u���āA�p�[�~�b�V������ 755 �ɐݒ肵�܂��B
#��   2. �u���E�U�Œ��ڃA�N�Z�X����ƃ`�F�b�N�t�H�[��������܂��̂ŁA
#��      �t�H�[�����Ƀ`�F�b�N������CGI�X�N���v�g�̃t�@�C���������
#��      ���܂��B�i�ʃf�B���N�g���ɂ���ꍇ�ɂ̓p�X�t���Ŏw��j
#��
#��	����(1) ����f�B���N�g������ test.cgi ���`�F�b�N
#��
#��		��  test.cgi �Ɠ���
#��
#��	����(2) ���s�̈ʒu�ɂ��� test�f�B���N�g������ test.cgi ��
#��             �`�F�b�N
#��
#��		��  ../test/test.cgi �Ɠ���
#��
#��   3. �`�F�b�N����CGI�X�N���v�g�̊g���q�� .cgi .pl .xcg ��3��
#��      �݂̂ł��B
#��
#�� [���ӎ���]
#��   1. ���̃v���O�����̓t���[�\�t�g�ł��B
#��   2. ���̃v���O�������g�p���������Ȃ鑹�Q�ɑ΂��č�҂͈�؂�
#��      �ӔC�𕉂��܂���B
#��������������������������������������������������������������������

#------------#
#  ��{�ݒ�  #
#------------#

# �p�X���[�h
# �� �p�����Ńp�X���[�h���w�肷��ƁA���̃v���O�����̎��s�ɂ�
#    �p�X���[�h���K�{�ƂȂ�܂��B(�p������8�����ȓ��Ŏw��)
$pass = '';

#------------#
#  �ݒ芮��  #
#------------#

print "Content-type: text/html\n\n";
print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size:13px; }
.red { color:#DD0000; }
.silver { background:#e0e0e0; }
A:link    { text-decoration:none; }
A:visited { text-decoration:none; }
A:active  { text-decoration:none; }
A:hover   { text-decoration:underline; color:#DD0000; }
-->
</STYLE>
<title>$ver</title></head>
<body bgcolor="white" text="black" link="blue" vlink="blue">
<center><hr width=400>
EOM

if ($ENV{'REQUEST_METHOD'} eq "POST") {
	read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
}
@buf = split(/&/, $buf);
foreach (@buf) {
	($key, $val) = split(/=/);
	$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$val =~ s/\0//g;
	$val =~ s/\+//g;
	$val =~ s/&//g;
	$val =~ s/"//g;
	$val =~ s/>//g;
	$val =~ s/<//g;

	$in{$key} = $val;
}
$file = $in{'file'};

# �p�X�`�F�b�N
if ($pass ne '') {
	if ($in{'pass'} eq '') {
		print "<P>�p�X���[�h����͂��Ă�������\n";
		print "<form action=\"pcheck.cgi\" method=\"POST\">\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=\" �F�� \"></form>\n";
		print "<hr width=400></center>\n</body></html>\n";
		exit;
	}
	elsif ($in{'pass'} ne $pass) {
		&error('<pre>�p�X���[�h���Ⴂ�܂�');
	}
}

print <<"EOM";
<h3>Perl���@�`�F�b�J�[</h3>
<table><tr><td>
<UL>
<LI>�t�H�[�����Ƀ`�F�b�N����t�@�C��������͂��Ă��������B
<LI>�g���q�� <tt>.cgi .pl .xcg</tt> �̂ݗL���ł��B
<P>syntax OK ���@���@�㐳����<br>
syntax error ���@���@�G���[
</UL>
</td></tr></table>
<form action="pcheck.cgi" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=text name=file size=35 value="$file">
<input type=submit value="�`�F�b�N">
<P>
EOM

if ($in{'file'}) {

	print "<span class=silver><b>- �f�f���� -</b></span><br><br>\n";

	# �t�@�C���`�F�b�N
	if ($file !~ /^[\.\/\w\-]+\.(cgi|pl|xcg)$/) {
		&error("�t�@�C�������s���ł� �� $file");
	}
	unless (-e $file) { &error('�t�@�C�������݂��܂���'); }

	# �擪�s�ǂݎ��
	open(IN,"$file");
	$top = <IN>;
	close(IN);

	print "<table border=1 cellpadding=8 cellspacing=1>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>���s�`��</font></td>";
	print "<td bgcolor='#FFFFCC'>";

	# ���s����
	if ($top =~ /(.*)\x0D\x0A$/) { print "CR+LF (Win�`��)"; $ppath = $1; }
	elsif ($top =~ /(.*)\x0D$/) { print "CR�iMac�`��)"; $ppath = $1; }
	elsif ($top =~ /(.*)\x0A$/) { print "LF (UNIX�`��)"; $ppath = $1; }
	else { print "�s��"; $ppath = '�s��'; }
	print "</td></tr>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>Perl�̃p�X</font></td>\n";
	print "<td bgcolor='#FFFFCC'><TT>$ppath</TT></td></tr>\n";
	print "<tr><td bgcolor='#0000DD'><font color='white'>�T�[�o��Perl<br>�Ƃ̃`�F�b�N</font></td>";
	print "<td bgcolor='#FFFFCC'>";

	# �p�X�`�F�b�N
	$ppath =~ s/^\#\!\s*//g;
	if (-e $ppath) { print "�����Ă��܂�<br><TT>$ppath</TT></td></tr>\n"; }
	else { print "�p�X���s���̂悤�ł�<br><TT>$ppath</TT></td></tr>\n"; }

	# �p�[�~�b�V����
	print "<tr><td bgcolor='#0000DD'><font color='white'>�p�[�~�b�V����</font></td>";
	print "<td bgcolor='#FFFFCC'>";
	if (-x $file) { print "���s������</td></tr>\n"; }
	else { print "���s��������܂���</td></tr>\n"; }

	# ���@�`�F�b�N
	print "<tr><td bgcolor='#0000DD'><font color='white'>���@�`�F�b�N</font></td>";
	print "<td bgcolor='#FFFFCC'>";
	print "<PRE CLASS=red>\n";

	# �`�F�b�N���s
	open(PROC,"perl -c $file 2>&1 |");
	print <PROC>;
	close(PROC);

	print "</PRE></td></tr></table>\n";
}

print <<"EOM";
<P><hr width=400>
<P><span style="font-family:verdana;font-size:11px;"><b>$ver</b><br>
<!-- ���쌠�\\�L�F�폜�֎~ -->
Copyright (C)
<a href='http://www.kent-web.com/'>Kent Web</a>
 2002
</span></center>
</body>
</html>
EOM
exit;

## �G���[����
sub error {
	print <<"EOM";
<P>$_[0]
</PRE>
<P><hr width=400></center>
</body>
</html>
EOM
	exit;
}

__END__

