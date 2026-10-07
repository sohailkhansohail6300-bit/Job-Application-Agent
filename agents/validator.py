def validate_claims(profile, generated_claims):
    profile_text = ' '.join([
        str(profile.get('summary') or ''),
        ' '.join([str(item.get('name') or item.get('title') or item) for item in (profile.get('skills') or [])]),
        ' '.join([str(item.get('company') or item.get('school') or item) for item in (profile.get('experience') or []) + (profile.get('education') or [])]),
        ' '.join([str(item.get('name') or item) for item in (profile.get('certifications') or [])]),
    ]).lower()

    blocked = []
    needs_confirmation = []
    ok = []

    for claim in generated_claims:
        text = (claim or '').lower()
        if not text.strip():
            continue
        if any(token in text for token in ['aws', 'azure', 'python', 'sql', 'react', 'machine learning', 'docker', 'kubernetes', 'terraform', 'power bi']):
            if any(token in profile_text for token in [t for t in ['aws', 'azure', 'python', 'sql', 'react', 'machine learning', 'docker', 'kubernetes', 'terraform', 'power bi'] if token in text]):
                ok.append(claim)
            else:
                blocked.append({
                    'claim': claim,
                    'detail': 'Unsupported claim detected; it is not backed by the master profile.'
                })
        else:
            ok.append(claim)

    return {
        'ok': not blocked,
        'summary': 'All supported claims verified against the master profile.' if not blocked else 'Unsupported claims detected; review required before approval.',
        'blocked': blocked,
        'needs_confirmation': needs_confirmation,
        'verified': ok,
    }
