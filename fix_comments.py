from pathlib import Path
import re

path = Path(r"d:\VS Projects\Maxi's Boutique\Boutique\Home.html")
text = path.read_text(encoding='utf-8')
lines = text.splitlines()

comment_pattern = re.compile(r'/\*.*?\*/|<!--.*?-->')
leading_comment_line = re.compile(r'^(?P<indent>\s*)(?P<lead>(?:/\*.*?\*/\s*|<!--.*?-->\s*)+)(?P<rest>.*)$')
trailing_comment_line = re.compile(r'^(?P<code>.*?)(?P<trail>(?:/\*.*?\*/\s*|<!--.*?-->\s*))\s*$')

pending_comments = []
output = []
for line in lines:
    if line.strip() == '':
        output.append(line)
        continue
    m_lead = leading_comment_line.match(line)
    if m_lead:
        lead = m_lead.group('lead')
        rest = m_lead.group('rest')
        comments = comment_pattern.findall(lead)
        if rest.strip() == '':
            pending_comments.extend(comments)
            continue
        line = m_lead.group('indent') + rest.rstrip()
        pending_comments.extend(comments)
    m_trail = trailing_comment_line.match(line)
    if m_trail and m_trail.group('code').strip() != '':
        code = m_trail.group('code').rstrip()
        trail_comments = comment_pattern.findall(m_trail.group('trail'))
    else:
        code = line.rstrip()
        trail_comments = []
    if pending_comments:
        all_comments = trail_comments + pending_comments
        line = code + ' ' + ' '.join(all_comments)
        pending_comments = []
    elif trail_comments:
        line = code + ' ' + ' '.join(trail_comments)
    output.append(line)

for c in pending_comments:
    output.append(c)

path.write_text('\n'.join(output), encoding='utf-8')
print('done')
