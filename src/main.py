import click
from src.etl.pipeline import ETLPipeline
from src.ranking.matcher import ResumeJobMatcher


@click.group()
def cli():
    """Resume-Job Matcher CLI"""
    pass

@cli.command()
def run_etl():
    """Run the ETL pipeline"""
    click.echo("Running ETL pipeline...")
    pipeline = ETLPipeline()
    resumes_df, jobs_df = pipeline.run_etl()
    click.echo(f"Processed {len(resumes_df)} resumes and {len(jobs_df)} jobs")

@cli.command()
@click.option('--top-k', default=5, help='Number of top matches to return')
def calculate_matches(top_k):
    """Calculate resume-job matches"""
    click.echo("Calculating matches...")
    matcher = ResumeJobMatcher()
    matches_df = matcher.calculate_matches(top_k=top_k)
    click.echo(f"Generated {len(matches_df)} matches")

@cli.command()
@click.option('--resume', required=True, help='Resume filename')
@click.option('--top-k', default=5, help='Number of top matches to show')
def show_matches(resume, top_k):
    """Show top matches for a specific resume"""
    matcher = ResumeJobMatcher()
    matches = matcher.get_top_matches_for_resume(resume, top_k)
    
    if matches.empty:
        click.echo(f"No matches found for {resume}")
        return
    
    click.echo(f"\nTop {top_k} matches for {resume}:")
    click.echo("-" * 50)
    
    for _, match in matches.iterrows():
        click.echo(f"{match['rank']}. {match['title']} at {match['company']}")
        click.echo(f"   Score: {match['combined_score']:.3f}")
        click.echo()

@cli.command()
def summary():
    """Show summary of all matches"""
    matcher = ResumeJobMatcher()
    summary_df = matcher.get_match_summary()
    
    if summary_df.empty:
        click.echo("No matches found. Run 'calculate-matches' first.")
        return
    
    click.echo("\nMatch Summary:")
    click.echo("-" * 60)
    
    current_resume = None
    for _, row in summary_df.iterrows():
        if current_resume != row['resume']:
            current_resume = row['resume']
            click.echo(f"\n{current_resume}:")
        
        click.echo(f"  {row['rank']}. {row['job_title']} at {row['company']} "
                  f"(Score: {row['combined_score']:.3f})")

if __name__ == '__main__':
    cli()