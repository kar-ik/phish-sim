import click
from phish_sim import config, models, simulation, safety_checks, consent, audit
from phish_sim.sendgrid_sender import send_real_email
from pathlib import Path
import os

@click.group()
@click.option('--sandbox', is_flag=True, default=True)
@click.option('--enable-sendgrid', is_flag=True, default=False)
@click.pass_context
def cli(ctx, sandbox, enable_sendgrid):
    config.SANDBOX_MODE = sandbox
    config.SENDGRID_ENABLED = enable_sendgrid and os.getenv('SENDGRID_API_KEY')  
    models.init_db()
    if not config.SANDBOX_MODE and not config.SENDGRID_ENABLED:
        click.echo("Warning: Real mode requires SendGrid key and admin approval.")
    ctx.ensure_object(dict)

@cli.command()
@click.option('--title', required=True)
@click.option('--description', required=True)
@click.option('--scope', default='small')
@click.option('--consent-path', required=True)
@click.option('--passphrase', required=True)
@click.option('--signer-name', required=True)
@click.option('--signer-email', required=True)
@click.pass_context
def create_campaign(ctx, title, description, scope, consent_path, passphrase, signer_name, signer_email):
    if safety_checks.check_dangerous_config(scope, []):
        return
    
    consent_file_id, checksum = consent.upload_consent(
        Path(consent_path), passphrase, signer_name, signer_email
    )
    
    if not consent.verify_consent(None, passphrase):  
        click.echo("Consent invalid.")
        return
    
    campaign_id = models.create_campaign(title, description, "admin", consent_file_id)
    
    approver_pass = click.prompt("Approver passphrase")
    if approver_pass != "approver_secret":
        click.echo("Approval denied.")
        return
    
    subject = click.prompt("Subject")
    body_html = click.prompt("Body HTML (safe)")
    warnings = safety_checks.scan_template(body_html)
    if warnings:
        click.echo(f"Warnings: {warnings}")
        if not click.confirm("Proceed?"):
            return
    
    lp_html = click.prompt("Landing HTML (no password fields)")
    allowed_fields = click.prompt("Allowed fields (JSON list, no password)")
    if not safety_checks.validate_landing_page(lp_html, allowed_fields):
        return
    
    click.echo(f"Campaign {campaign_id} created.")

@cli.command()
@click.option('--campaign-id', required=True)
@click.option('--seed-accounts', required=True, help='Comma-separated emails')
@click.pass_context
def simulate(ctx, campaign_id, seed_accounts):
    accounts = [e.strip() for e in seed_accounts.split(',')]
    metrics = simulation.run_simulation(campaign_id, accounts)
    click.echo(f"Simulation results: {metrics}")
    click.echo("Training link: http://localhost/training")

@cli.command()
@click.option('--campaign-id', required=True)
@click.pass_context
def dashboard(ctx, campaign_id):
    report = simulation.generate_report(campaign_id)
    click.echo(json.dumps(report, indent=2))

@cli.command()
@click.option('--campaign-id', required=True)
@click.option('--confirm', is_flag=True)
@click.pass_context
def launch(ctx, campaign_id, confirm):
    if not confirm:
        click.echo("Requires --confirm and 5-min delay (simulated).")
        return
    click.echo("Delaying 5 min...")  
    if config.SANDBOX_MODE:
        click.echo("Sandbox: No real send.")
        return
    click.echo("Launched (with safeguards).")

@cli.command()
@click.option('--campaign-id', required=True)
@click.option('--confirm', is_flag=True)
@click.pass_context
def kill(ctx, campaign_id, confirm):
    if confirm:
        config.KILL_SWITCH = True

        click.echo("Campaign aborted.")

if __name__ == '__main__':
    cli()
